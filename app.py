from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)

# ✅ Hardcoded credentials for local testing (DANGER: Don't expose in public repos!)
MICROSOFT_APP_ID = "e74046ec-9851-4219-a94f-a5cdf3f19e8a"
MICROSOFT_APP_PASSWORD = "223acc1e-63b7-4634-9f3c-0bbafcf70ec6"

print("✅ MicrosoftAppId loaded:", MICROSOFT_APP_ID)
print("✅ MicrosoftAppPassword loaded:", MICROSOFT_APP_PASSWORD)

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

        # Send reply to Bot Framework
        conversation_id = data["conversation"]["id"]
        service_url = data["serviceUrl"]
        post_url = f"{service_url}v3/conversations/{conversation_id}/activities"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_bot_token()}"
        }

        response = requests.post(post_url, json=reply_activity, headers=headers)
        print(f"📤 Sent to Bot Framework: {response.status_code} - {response.text}")

        return '', 200

    return jsonify({}), 200

def get_bot_token():
    url ="https://login.microsoftonline.com/8695b83d-c692-47ef-ad7a-376cbce3664f/oauth2/v2.0/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': MICROSOFT_APP_ID,
        'client_secret': MICROSOFT_APP_PASSWORD,
        'scope': 'https://api.botframework.com/.default'
    }

    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

    response = requests.post(url, data=payload, headers=headers)
    print("🔐 Token Response:", response.status_code, response.text)

    if response.status_code != 200:
        return None

    return response.json().get("access_token")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
