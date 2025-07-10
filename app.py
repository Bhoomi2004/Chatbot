from flask import Flask, request, jsonify

app = Flask(__name__)

qa_data = {
    "what is azure?": "Azure is Microsoft's cloud computing platform.",
    "what is qna bot?": "A QnA bot answers user questions using predefined data.",
    "hello": "Hi! I'm your QnA assistant. Ask me something.",
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.json
    user_message = data.get("text") or data.get("value", "") or ""
    if not user_message and "type" in data and data["type"] == "message":
        user_message = data.get("text", "")  # fallback

    response = qa_data.get(user_message.lower(), "Sorry, I don't understand that yet.")
    return jsonify({
        "type": "message",
        "text": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978)
