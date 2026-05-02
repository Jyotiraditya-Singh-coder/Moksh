import os
import mysql.connector
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fetch_training_data():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", "1234"),
            database=os.environ.get("MYSQL_DATABASE", "moksh_db")
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Fetch from dropout_training_data or any other target table
            cursor.execute("SELECT * FROM dropout_training_data LIMIT 50")
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def generate_rag_response(query: str) -> str:
    # 1. Fetch data from MySQL
    data = fetch_training_data()
    
    # 2. Format Context
    context = "Training Data Context:\n"
    for row in data:
        context += f"Student Data - Attendance: {row.get('attendance_rate')}, Score: {row.get('avg_test_score')}, Time: {row.get('engagement_time')}, Assignments: {row.get('assignment_completion')}, Weak Topics: {row.get('weak_topics_count')}, Risk Level: {row.get('risk')}\n"

    # 3. Create Groq Prompt
    prompt = f"Using the following context from our SQL training database, answer the user's query.\n\nContext:\n{context}\n\nQuery: {query}\n\nAnswer:"
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting Groq API: {e}"
