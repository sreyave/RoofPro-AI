from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

# Landing Page
@home_bp.route("/")
def home():
    return render_template("home.html")


# Chatbot Page (your existing index.html)
@home_bp.route("/chat")
def chat_page():
    return render_template("index.html")
