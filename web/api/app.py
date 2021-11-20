from flask import Flask

from .static import static
from .webhooks import messenger
from .webhooks import sms

app = Flask(__name__)

app.register_blueprint(messenger)
app.register_blueprint(sms)
app.register_blueprint(static)
