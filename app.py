from flask import Flask, request, jsonify

app = Flask(__name__)

qa_data = {
    "hello": "Hi! I'm your QnA assistant. Ask me something.",
    "what is azure?": "Azure is Microsoft's cloud computing platform.",
    "what is qna bot?": "A QnA bot answers user questions using predefined data.",
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.get_json(force=True)

    # The Bot Framework sends different activity types. Only respond to "message"
    if data.get("type") == "message":
        user_message = data.get("text", "").strip().lower()

        # Match from predefined answers
        response_text = qa_data.get(user_message, "Sorry, I don't understand that yet.")

        # Construct and return a bot response
        return jsonify({
            "type": "message",
            "text": response_text
        })
    
    # Respond 200 OK to non-message activities
    return jsonify({}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
