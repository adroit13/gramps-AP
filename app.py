import os
import sqlite3
import json  # Import the json module
from flask import Flask, jsonify, request, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
DATABASE_URL = os.environ.get("USER_DB_URI", "/app/data/users.sqlite")
DATABASE_DIR = os.path.dirname(DATABASE_URL)  # Extract directory

# Create Database Directory (if it doesn't exist)
if not os.path.exists(DATABASE_DIR):
    try:
        os.makedirs(DATABASE_DIR, exist_ok=True)  # Create directory, ignore if exists
        print(f"Created directory: {DATABASE_DIR}")  # Log the creation
    except OSError as e:
        print(f"Error creating directory {DATABASE_DIR}: {e}")  # Log any errors

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

# Ensure the database file exists
if not os.path.exists(DATABASE_URL):
    conn = sqlite3.connect(DATABASE_URL)
    conn.close()

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
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get database schema version (assuming PRAGMA user_version)
        cursor.execute("PRAGMA user_version;")
        db_schema_version = cursor.fetchone()[0]

        # Define API version
        api_version = "0.1.0"  # You might want to store this elsewhere

        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        initial_setup_needed = user_count == 0

        conn.close()

        return jsonify({
            "status": "success",
            "message": "API metadata available",
            "data": {
                "database": {
                    "schema_version": db_schema_version
                },
                "gramps_webapi": {
                    "version": api_version
                },
                "initial_setup_needed": initial_setup_needed
            }
        })
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"status": "error", "message": "Error fetching metadata", "details": str(e)}), 500

@app.route("/api/translations/en", methods=["GET", "POST"])
def translations():
    if request.method == "POST":
        return jsonify({"status": "success", "message": "Translation data received"}), 200
    else:  # GET request
        try:
            # Load translation data from a JSON file (or database)
            with open("translations_en.json", "r") as f:
                translation_data = json.load(f)
            return jsonify(translation_data), 200
        except FileNotFoundError:
            return jsonify({"status": "error", "message": "Translation file not found"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": "Error loading translations", "details": str(e)}), 500

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
        try:
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return jsonify([dict(row) for row in users]), 200
        except Exception as e:
            return jsonify({'error': 'Database error', 'details': str(e)}), 500
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

@app.route("/api/setup/", methods=["POST"])
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
