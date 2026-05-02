import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Update user and password with your MySQL server credentials
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234' # Using the password from your last command, change if different
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read the SQL file
            with open('moksh_db.sql', 'r') as file:
                sql_script = file.read()
            
            # Split the script into separate commands
            sql_commands = sql_script.split(';')
            
            for command in sql_commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                        print(f"Executed: {command.strip()[:50]}...")
                    except Error as e:
                        print(f"Error executing command: {e}")
            
            connection.commit()
            print("Database setup completed successfully.")
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == '__main__':
    create_database()
