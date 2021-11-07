## PSN Technical Exercise

Ingest sample data into a SQL database, and create a REST API with Python and Flask.

### `create_db.py`
    
- Reads SampleData.csv into a SQLite database (chosen because it's lightweight and easily integrated with Python)
- Deals with encoding error by removing bad characters. This could also be fixed by passing a different
encoding argument to Pandas. I chose the former because I felt it resulted in a cleaner set of data with no special characters, that could cause further issues down the line.
- Prints the row and column count to the console.
- `query_db` reads a .sql file from the specified filepath and runs it against the SQLite connection. I used this to create the aggregated table `creator`, and wrote it to 
be dynamic so it has potential for other applications.
- **Potential Improvements**
    - Add option to pass query string to `query_db`, as well as filepath.
    - `logging.log` would be a better choice than `print` for production code.
  
### `store_api.py`

- Uses Flask to expose the `product` table as a REST API
- The API has several endpoints, accepting `GET`, `DELETE`, and `PUT` methods to query and alter the database
- **Potential improvements**
    - SQLite results with more than one field are returned as a list by default - could be improved by formatting as key/value pairs. Needs more testing to establish the most efficient method.
    - Build error handling for bad requests
    - Add authorisation requirement and/or IP address restriction