from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "GrampsWeb API is running!"

@app.route("/api/metadata/")
def metadata():
    return jsonify({"status": "success", "message": "API metadata available"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
