import csv
import mysql.connector

# File path configurations
csv_file_path = r'C:\Users\prave\OneDrive\Desktop\Moksh\backend\ai-services\dropout-model\training_data.csv'

def import_csv_to_mysql():
    try:
        # Connect to MySQL Database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='moksh_db'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 1. Create table structured for the dropout model
            create_table_query = """
            CREATE TABLE IF NOT EXISTS dropout_training_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                attendance_rate FLOAT,
                avg_test_score FLOAT,
                engagement_time FLOAT,
                assignment_completion FLOAT,
                weak_topics_count INT,
                risk INT
            );
            """
            cursor.execute(create_table_query)
            print("Table 'dropout_training_data' ensured.")
            
            # Optional: Clear the table if you want to replace it entirely
            # cursor.execute("TRUNCATE TABLE dropout_training_data;")

            # 2. Read data from CSV
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)  # Skip validation headers
                print(f"Detected columns: {headers}")

                # Prepare the insertion query
                insert_query = """
                INSERT INTO dropout_training_data 
                (attendance_rate, avg_test_score, engagement_time, assignment_completion, weak_topics_count, risk)
                VALUES (%s, %s, %s, %s, %s, %s)
                """

                # 3. Batch parse and insert
                records = []
                for row in csv_reader:
                    # Convert strings to right formats: float, float, float, float, int, int
                    records.append((
                        float(row[0]),
                        float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        int(row[4]),
                        int(row[5])
                    ))

                # Use executemany for faster batch insertion
                if records:
                    cursor.executemany(insert_query, records)
                    connection.commit()
                    print(f"Successfully inserted {cursor.rowcount} rows into the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"General Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    import_csv_to_mysql()
