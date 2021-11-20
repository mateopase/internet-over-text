from flask import Flask, request

app = Flask(__name__)

@app.route("/sms/reply", methods=["POST"])
def handle_sms():
    return "Hello"