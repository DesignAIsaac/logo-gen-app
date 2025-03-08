from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Database setup
MONGO_URI = "mongodb://admin:strongpassword@localhost:27017/logogen?authSource=admin"
client = MongoClient(MONGO_URI)
db = client.logogen
users_collection = db.users
questionnaire_collection = db.questionnaires

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Logo Generator API"})

if __name__ == '__main__':
    app.run(debug=True)

