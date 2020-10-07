from flask_restx import Api
from .max_threshold import api as max_threshold_api
from .desired_properties import api as desired_properties_api

api = Api(title="Api", version="1.0", description="Prototype")
api.add_namespace(max_threshold_api)
api.add_namespace(desired_properties_api)

