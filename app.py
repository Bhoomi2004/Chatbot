from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import uuid
import datetime

app = Flask(__name__)
CORS(app)

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

        # Construct the reply message as per Bot Framework schema
        reply_activity = {
            "type": "message",
            "from": {
                "id": data["recipient"]["id"],
                "name": data["recipient"].get("name", "bot")
            },
            "recipient": {
                "id": data["from"]["id"],
                "name": data["from"].get("name", "")
            },
            "replyToId": data["id"],
            "text": response_text,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

        # Send the reply back to the serviceUrl
        conversation_id = data["conversation"]["id"]
        service_url = data["serviceUrl"]
        post_url = f"{service_url}v3/conversations/{conversation_id}/activities"

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(post_url, json=reply_activity, headers=headers)
        print(f"📤 Sent to Bot Framework: {response.status_code} - {response.text}")

        return '', 200

    return jsonify({}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
