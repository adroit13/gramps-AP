from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Explicitly enabling CORS for all /api/* routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "GrampsWeb API is running!"

@app.route("/api/metadata/")
def metadata():
    return jsonify({"status": "success", "message": "API metadata available"})

# Fix: Add this route to handle the frontend request
@app.route("/api/translations/en", methods=["POST"])
def translations():
    return jsonify({"message": "Translation data received", "status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
