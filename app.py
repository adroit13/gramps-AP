from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

# ✅ NEW ROUTES (Fixing 404 Errors)
@app.route("/api/events/")
def events():
    return jsonify({"status": "success", "events": []})  # Returns an empty list for now

@app.route("/api/search/")
def search():
    return jsonify({"status": "success", "results": []})  # Empty search results for now

@app.route("/api/sources/")
def sources():
    return jsonify({"status": "success", "sources": []})  # Empty sources for now

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
