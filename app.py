from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["https://webchat.botframework.com"])

qa_data = {
    "hello": "Hi there! I'm your chatbot.",
    "what is azure?": "Azure is Microsoft's cloud platform for building, testing, and managing applications.",
    "what is ai?": "AI stands for Artificial Intelligence, which enables machines to mimic human intelligence.",
    "bye": "Goodbye! Have a great day!"
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.get_json(force=True)
    print("📨 Received request:", data)

    if data.get("type") == "message":
        user_message = data.get("text", "").strip().lower()
        print("🧠 User said:", user_message)

        response_text = qa_data.get(user_message, "Sorry, I don't understand that question.")
        print("💬 Responding with:", response_text)

        return jsonify({
            "type": "message",
            "text": response_text
        })

    print("⚙️ Received non-message activity type:", data.get("type"))
    return jsonify({}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
