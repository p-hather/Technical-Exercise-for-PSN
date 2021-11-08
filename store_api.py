from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def execute_query(query, args=None):
    """
    Used to execute a query against the db, and return the results.
    """
    conn = sqlite3.connect('store.db', check_same_thread=False)
    cursor = conn.cursor()

    if args:
        cursor.execute(query, args)
    else:
        cursor.execute(query)
    results = cursor.fetchall()

    conn.commit()  # Commit changes for DDL queries
    conn.close()  # Close connection
    return results


@app.route('/locations', methods=["GET"])
def get_locations():
    """
    Get all distinct locations in the product table.
    """
    query = '''
        select distinct
            location
        from
            product
        '''
    results = execute_query(query)
    return jsonify({"locations": results})


@app.route('/creator/<creator_id>', methods=["GET", "DELETE"])
def manage_creator(creator_id):
    """
    Accepts both GET and DELETE methods, with a creator ID passed in the URL.
    GET requests return all the creator's rows as JSON, whereas DELETE removes
    all creator rows from the product table.
    """
    if request.method == 'GET':
        query = f'''
            select
                *
            from
                product
            where
                creatorID = ?
            '''
        results = execute_query(query, [creator_id])
        return jsonify(results)

    elif request.method == 'DELETE':
        query = f'''
                delete from product
                where
                    creatorID = ?
                '''
        execute_query(query, [creator_id])
        return jsonify(f'Successfully deleted products from creator with ID {creator_id}')


@app.route('/product/update_price', methods=["PUT"])
def update_prices():
    """
    Update the prices for a given product.

    Accepts JSON in the format -
    {"Index": int,
    "profit": float,
    "revenue": float,
    "cost": float}
    """

    product = request.get_json()
    query = '''
        update product
        set
            profit = ?,
            revenue = ?,
            cost = ?
        where
            "Index" = ?
        '''
    execute_query(query, [product["profit"], product["revenue"], product["cost"], product["Index"]])
    return jsonify(f'Successfully updated prices for product {product["Index"]}')


if __name__ == '__main__':
    app.run(debug=True)
