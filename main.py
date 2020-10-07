from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from endpoints import api

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = False

api.init_app(app)