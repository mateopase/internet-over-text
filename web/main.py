from flask import Flask

app = Flask(__name__)

@app.route("/sms")
def handle_sms():
    return "Hello"