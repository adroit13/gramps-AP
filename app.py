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

# ✅ ADD MISSING ROUTES
@app.route("/api/users/-/")
def users():
    return jsonify({"status": "success", "users": []})  # Placeholder response

@app.route("/api/pagesize")
def pagesize():
    return jsonify({"status": "success", "pagesize": 10})  # Placeholder value

@app.route("/api/pages")
def pages():
    return jsonify({"status": "success", "pages": []})  # Placeholder response

@app.route("/api/roles")
def roles():
    return jsonify({"status": "success", "roles": ["admin", "editor", "viewer"]})  # Example roles

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
