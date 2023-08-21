import cx_Oracle

# Set your connection parameters
username = 'ORIENTADOR'
password = 'ofulp2023'
hostname = '10.14.12.164'
port = '1521'
sid = 'NEWFULP'

# Create a connection string
dsn = cx_Oracle.makedsn(hostname, port, sid=sid)

# Establish the connection
connection = cx_Oracle.connect(username, password, dsn)

# Create a cursor to interact with the database
cursor = connection.cursor()

# Example query
query = "SELECT * FROM ORIENTADOR.CONTROL_PROCESOS"

# Execute the query
cursor.execute(query)

# Fetch and print results
for row in cursor.fetchall():
    print(row)

# Close the cursor and the connection
cursor.close()
connection.close()
