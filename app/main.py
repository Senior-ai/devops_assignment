from flask import Flask, request, make_response
import mysql.connector
import time
import socket

app = Flask(__name__)

def create_db_connection():
    db = None
    while db is None:
        try:
            db = mysql.connector.connect(
                host="mysql_container",
                user="root",  
                password="root",
                port="3306"
            )
            cursor = db.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
            db.database = "mydatabase"

        except mysql.connector.Error as err:
            print("Error connecting to MySQL: {}".format(err))
            print("Retrying in 5 seconds...")
            time.sleep(5)
    return db

db = create_db_connection()

cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS counter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    count INT DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    client_ip VARCHAR(15),
    server_ip VARCHAR(15)
)
""")

@app.route('/')
def index():
    cursor.execute("SELECT count FROM counter WHERE id = 1")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO counter (id, count) VALUES (1, 1)")
        count = 1
    else:
        count = result[0] + 1
        cursor.execute("UPDATE counter SET count = %s WHERE id = 1", (count,))
    db.commit()

    # Record access log
    server_ip = socket.gethostbyname(socket.gethostname())
    cursor.execute("INSERT INTO access_log (client_ip, server_ip) VALUES (%s, %s)", (request.remote_addr, server_ip))
    db.commit()

    # Set the cookie
    response = make_response(server_ip)
    response.set_cookie('internal-IP', server_ip, max_age=60*5)

    return response

@app.route('/showcount')
def show_count():
    cursor.execute("SELECT count FROM counter WHERE id = 1")
    result = cursor.fetchone()
    return str(result[0]) if result else '0'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)
