import pandas as pd
import sqlite3


def csv_to_sqlite(csv_fp, connection, tbl_name):
    """Reads CSV from given filepath and writes to a SQLite database"""
    try:
        df = pd.read_csv(csv_fp)
    except UnicodeDecodeError:  # CSV contains encoded special characters (poss written from Excel)
        print(f'Warning - encoding error discovered in {csv_fp}, removing bad characters and proceeding')
        df = pd.read_csv(csv_fp, index_col='Index', encoding_errors='ignore')
        # Could also use "encoding='ISO-8859–1'" arg but preferred removal of special characters ready for db
    print(f'Dataframe contains {len(df)} rows and {len(df.columns)} columns - headers are:\n{list(df.columns)}')
    df.to_sql(index_label='Index', name=tbl_name, con=conn, if_exists='replace')
    # Set to replace for dev purposes
    print('Dataframe successfully loaded to SQLite database')


def execute_query(connection, sql_fp, ddl=False):
    """Executes a query against a SQLite database, returns the results as a dataframe, unless DDL"""
    with open(sql_fp, 'r') as file:
        query = file.read()
    print(f'Executing query:\n{query}')
    if ddl:
        # if DDL arg specified, return a success statement
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print('DDL successfully committed to database')
    else:
        # Otherwise return the results as a dataframe
        return pd.read_sql(query, connection)


if __name__ == '__main__':
    conn = sqlite3.connect('store.db')
    csv_to_sqlite('./SampleData.csv', conn, 'product')
    execute_query(conn, './creator.sql', ddl=True)
    conn.close()
