import os
import traceback
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    # Reload dotenv so changes to .env file are reflected dynamically
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or "your_groq_api_key" in api_key:
        return jsonify({"error": "GROQ_API_KEY is missing or invalid in your .env file."}), 400

    try:
        client = Groq(api_key=api_key)
        data = request.json
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "No messages provided."}), 400

        # Request to Groq
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("--- ERROR OCCURRED IN CHAT API ---")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
