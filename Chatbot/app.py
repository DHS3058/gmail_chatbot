from flask import Flask, request, jsonify, render_template
# from langchain.llms import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
import os

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = "AIzaSyBv-7b-YuXwBSeZyCdI0wz7DAkxqOpYm-w"  # API key
llm = GoogleGenerativeAI(model="gemini-pro")

# Function to generate chatbot response
def get_chat_response(user_input):
    response = llm.predict(user_input)
    return response

# Home route to serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    bot_response = get_chat_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
