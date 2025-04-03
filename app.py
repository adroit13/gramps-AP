import os
import sqlite3
from flask import Flask, jsonify, request, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
DATABASE_URL = os.environ.get("USER_DB_URI", "users.db")

# Ensure the database file exists
if not os.path.exists(DATABASE_URL):
    conn = sqlite3.connect(DATABASE_URL)
    conn.close()


# Database Connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


# Error Handling
@app.teardown_appcontext
def close_db_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# API Endpoints
@app.route("/")
def home():
    return "GrampsWeb API is running!"


@app.route("/api/metadata/")
def metadata():
    return jsonify({"status": "success", "message": "API metadata available"})


@app.route("/api/translations/en", methods=["GET", "POST"])
def translations():
    if request.method == "POST":
        return jsonify({"status": "success", "message": "Translation data received"}), 200
    return jsonify({"status": "success", "message": "Translation data endpoint"}), 200


@app.route("/api/events/")
def events():
    return jsonify({"status": "success", "events": []})


@app.route("/api/search/")
def search():
    return jsonify({"status": "success", "results": []})


@app.route("/api/sources/")
def sources():
    return jsonify({"status": "success", "sources": []})


@app.route("/api/users/", methods=['GET', 'POST'])
def api_users():
    conn = get_db_connection()
    if request.method == 'GET':
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return jsonify([dict(row) for row in users]), 200
    elif request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            conn.execute("INSERT INTO users (email) VALUES (?)", (email,))
            conn.commit()
            conn.close()
            return jsonify({'message': 'User added successfully'}), 201
        except KeyError as e:
            return jsonify({'error': 'Missing parameter', 'details': str(e)}), 400
        except sqlite3.Error as e:
            return jsonify({'error': 'Database error', 'details': str(e)}), 500
    else:
        conn.close()
        return jsonify({'error': 'Method not allowed'}), 405


@app.route("/api/setup/")
def setup_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        return jsonify({"message": "Database initialized successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": "Database initialization failed", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
