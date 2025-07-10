from flask import Flask, request, jsonify

app = Flask(__name__)

qa_data = {
    "what is azure?": "Azure is Microsoft's cloud computing platform.",
    "what is qna bot?": "A QnA bot answers user questions using predefined data.",
    "hello": "Hi! I'm your QnA assistant. Ask me something.",
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.json or {}
    
    if data.get("type") == "message":
        user_message = data.get("text", "").lower()
        response_text = qa_data.get(user_message, "Sorry, I don't understand that yet.")

        return jsonify({
            "type": "message",
            "text": response_text
        })
    
    # Respond with 200 OK to all non-message activities (like conversationUpdate)
    return jsonify({}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
