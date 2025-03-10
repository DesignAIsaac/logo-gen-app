from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId  # Import this to handle ObjectId serialization

app = Flask(__name__)

# Database setup
MONGO_URI = "mongodb+srv://admin-logo:xZrc04zgK@cluster0.xvu0t.mongodb.net/logogen?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.logogen
users_collection = db.users
questionnaire_collection = db.questionnaires

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Logo Generator API"})

# Endpoint to store questionnaire responses
@app.route('/save_questionnaire', methods=['POST'])
def save_questionnaire():
    data = request.json
    if not data.get("user_id") or not data.get("responses"):
        return jsonify({"error": "Missing user_id or responses"}), 400

    questionnaire_collection.insert_one(data)
    return jsonify({"message": "Questionnaire saved successfully"})

# Endpoint to retrieve questionnaire responses
@app.route('/get_questionnaire/<user_id>', methods=['GET'])
def get_questionnaire(user_id):
    responses = questionnaire_collection.find_one({"user_id": user_id}, {"_id": 0})
    if not responses:
        return jsonify({"error": "No questionnaire found for this user"}), 404
    return jsonify(responses)

# Endpoint to store generated logos
@app.route('/save_logo', methods=['POST'])
def save_logo():
    data = request.json
    if not data.get("user_id") or not data.get("logo_data"):
        return jsonify({"error": "Missing user_id or logo_data"}), 400

    db.designs.insert_one({
        "user_id": data["user_id"],
        "logo_data": data["logo_data"],
        "metadata": data.get("metadata", {})
    })
    return jsonify({"message": "Logo saved successfully"})

# ✅ FIXED FUNCTION: Endpoint to retrieve stored logos
@app.route('/get_logo/<user_id>', methods=['GET'])
def get_logo(user_id):
    logo = db.designs.find_one({"user_id": user_id})
    if not logo:
        return jsonify({"error": "No logo found for this user"}), 404

    # Convert ObjectId to string for JSON serialization
    logo["_id"] = str(logo["_id"])
    return jsonify(logo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

