
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))

db = client["flask_database"]
collection = db["submissions"]
todo_collection = db["todo_items"]


# Task 1: JSON API
@app.route('/api', methods=['GET'])
def get_data():

    try:
        with open('data.json', 'r') as file:
            data = json.load(file)

        return jsonify(data)

    except Exception:
        return jsonify({"error": "Unable to read data"}), 500


# Task 2: Receive form data and store in MongoDB
@app.route('/submit', methods=['POST'])
def submit_data():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        collection.insert_one({
            "name": name,
            "email": email
        })

        return jsonify({
            "message": "Data submitted successfully"
        }), 201

    except Exception:
        app.logger.exception("MongoDB insertion failed")

        return jsonify({
            "error": "Unable to save data to MongoDB"
        }), 500


@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({"error": "Both fields are required"}), 400

    todo_collection.insert_one({
        "itemName": item_name,
        "itemDescription": item_description
    })

    return jsonify({
        "message": "To-Do item submitted successfully"
    }), 201


if __name__ == '__main__':
    app.run(port=5001, debug=True)
