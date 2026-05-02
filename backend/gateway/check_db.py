import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='moksh_db'
    )
    
    if connection.is_connected():
        print("Successfully connected to 'moksh_db'!")
        cursor = connection.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Check users table schema
        if tables and 'users' in [t[0] for t in tables]:
            cursor.execute("DESCRIBE users;")
            columns = cursor.fetchall()
            print("\nSchema for 'users' table:")
            for col in columns:
                print(f"Field: {col[0]}, Type: {col[1]}")
                
        cursor.close()
        connection.close()
except Exception as e:
    print(f"Error: {e}")
