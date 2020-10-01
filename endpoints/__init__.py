from flask_restx import Api
from flask import Blueprint
from .max_threshold import api as max_threshold_api

blueprint = Blueprint('api', __name__, url_prefix='/domain_api/va')
api = Api(blueprint, title="Api", version="1.0", description="Prototype")

@api.errorhandler(Exception)
def error_handler(error):
    return {
      "status": 'failure',
      "code": 500,
      "message": str(error),
    }

api.add_namespace(max_threshold_api)


