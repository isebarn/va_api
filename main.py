from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from endpoints import blueprint as api

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = False
app.register_blueprint(api)
