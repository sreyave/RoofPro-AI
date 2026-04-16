from flask import Blueprint, request, jsonify
from app.services.chatbot_service import handle_chat

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = handle_chat(user_input)
    return jsonify({"reply": response})
