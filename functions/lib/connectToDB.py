# Connect to sql oracle database
import cx_Oracle

# Connect to DB: return cursor and connection
def connect(host, port, sid, user, password):
    # TODO: Need to sanitize the host, port, sid, user, and password and make them parameters
    # Set up the connection details
    dsn = cx_Oracle.makedsn(host, port , service_name=sid)
    # Establish a connection
    connection = cx_Oracle.connect(user, password, dsn)
    # Create a cursor to execute SQL statements
    cursor = connection.cursor()
    return cursor, connection

# Close the cursor and the connection
def close(cursor, connection):
    cursor.close()
    connection.close()

# Execute a query and return the rows
def getData(cursor, query):
    # TODO:  Need to sanitize the table name and the query
    # Execute a query
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

# Main process:
# 1. Read the connection parameters from the .env file
# 2. Connect to the database
# 3. Define the table and the query
# 4. Get the data from the database
