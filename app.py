from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample QnA pairs (you can replace these later)
qa_data = {
    "what is azure?": "Azure is Microsoft's cloud computing platform.",
    "what is qna bot?": "A QnA bot answers user questions using predefined data.",
    "hello": "Hi! I'm your QnA assistant. Ask me something.",
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.json
    user_message = data["text"].lower()

    # Match user message to QnA
    response = qa_data.get(user_message, "Sorry, I don't understand that yet.")

    return jsonify({
        "type": "message",
        "text": response
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3978)
