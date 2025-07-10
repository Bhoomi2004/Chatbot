from flask import Flask, request, jsonify

app = Flask(__name__)

qa_data = {
    "hello": "Hi there! I'm your chatbot.",
    "what is azure?": "Azure is Microsoft's cloud platform for building, testing, and managing applications.",
    "what is ai?": "AI stands for Artificial Intelligence, which enables machines to mimic human intelligence.",
    "bye": "Goodbye! Have a great day!"
}

@app.route("/api/messages", methods=["POST"])
def messages():
    data = request.get_json(force=True)

    # ✅ Handle messages only
    if data.get("type") == "message":
        user_message = data.get("text", "").strip().lower()

        # 🔍 Respond if known
        response_text = qa_data.get(user_message, "Sorry, I don't understand that question.")

        return jsonify({
            "type": "message",
            "text": response_text
        })

    # ℹ️ Return 200 OK for other activity types
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
