from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from langchain_google_genai import GoogleGenerativeAI
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Security key for session handling
CORS(app)

# Google API setup
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
os.environ["GOOGLE_API_KEY"] = "your_API"  # Replace with actual Google Gemini API key
llm = GoogleGenerativeAI(model="gemini-1.5-pro")

# Dictionary to store conversation history (in-memory, resets on restart)
conversation_history = {}

def authenticate_gmail():
    """Authenticate and return Gmail API service."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials3.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

gmail_service = authenticate_gmail()

@app.route("/fetch_opened_email", methods=["POST"])
def fetch_opened_email():
    """Fetch content of the currently opened email in Gmail and generate an AI response."""
    data = request.json
    email_content = data.get("email_content", "")
    email_subject = data.get("email_subject", "")
    email_sender = data.get("email_sender", "")

    if not email_content:
        return jsonify({"error": "No email content provided"}), 400

    # Generate AI response based on email content
    prompt = (
        f"You are an AI assistant. Generate a professional response to this email:\n\n"
        f"Sender: {email_sender}\n"
        f"Subject: {email_subject}\n"
        f"Email Content:\n{email_content}\n\n"
        "Response:"
    )

    ai_response = llm.predict(prompt)
    return jsonify({"response": ai_response})


def generate_response(user_id, user_input, email_content=None):
    """Generate an AI response based on user input while maintaining conversation history."""

    # Initialize user history if not present
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Maintain conversation context
    context = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in conversation_history[user_id]])
    prompt = f"{context}\nUser: {user_input}\nAI:"
    response = llm.predict(prompt).strip()

    # Append conversation to history
    conversation_history[user_id].append({"sender": "User", "message": user_input})
    conversation_history[user_id].append({"sender": "AI", "message": response})

    return response


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages from the chatbox with conversation memory."""
    data = request.json
    message = data.get("message", "").strip()
    user_id = data.get("user_id", "default_user")  # Unique ID to track users

    if not message:
        return jsonify({"error": "No message provided"}), 400

    response = generate_response(user_id, message)
    return jsonify({"response": response})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
