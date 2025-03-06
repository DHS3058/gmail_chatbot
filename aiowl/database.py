# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend interaction

# # MongoDB connection
# # client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb+srv://pragya:seKZJa1gUEz5RA9W@cluster0.skaxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client["client"]
# clients_collection = db["client_info"]

# # API to add a new client
# @app.route("/add-client", methods=["POST"])
# def add_client():
#     data = request.json

#     # Validate required fields
#     if not all(key in data for key in ["client_info", "client_poc", "manage_access"]):
#         return jsonify({"error": "Missing required fields"}), 400

#     # Insert into MongoDB
#     result = clients_collection.insert_one(data)

#     return jsonify({"message": "Client added successfully", "id": str(result.inserted_id)}), 201


# # API to get all clients
# @app.route("/clients", methods=["GET"])
# def get_clients():
#     clients = list(clients_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
#     return jsonify(clients)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from email_utils import send_email  # Import the send_email function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# MongoDB connection
client = MongoClient("mongodb+srv://pragya:seKZJa1gUEz5RA9W@cluster0.skaxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["client"]
clients_collection = db["client_info"]
users_collection = db["employee_info"]

# Function to send a message (placeholder for actual implementation)
def send_message(email, message):
    print(f"Sending message to {email}: {message}")

# API to add a new client
@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.json

    # Validate required fields
    if not all(key in data for key in ["client_info", "client_poc", "manage_access"]):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert into MongoDB
    result = clients_collection.insert_one(data)

    # Fetch email addresses for users in manage_access
    manage_access = data["manage_access"]
    manage_access_names = [manage_access["first_person"], manage_access["checker"]]
    emails = []
    for name in manage_access_names:
        user = users_collection.find_one({"name": name}, {"email": 1, "_id": 0})
        if user:
            emails.append(user["email"])
        else:
            print(f"No email found for user: {name}")

    # Log the fetched email addresses
    print(f"Fetched emails: {emails}")

    # Send messages to users
    for email in emails:
        send_message(email, "You have been added to this project.")
        send_email(email, "Project Assignment", "You have been added to this project.")

    return jsonify({"message": "Client added successfully", "id": str(result.inserted_id)}), 201

# API to get all clients
@app.route("/clients", methods=["GET"])
def get_clients():
    clients = list(clients_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
    return jsonify(clients)

if __name__ == "__main__":
    app.run(debug=True)