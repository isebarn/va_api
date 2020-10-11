from flask_restx import Api, fields
from .max_threshold import api as max_threshold_api
from .desired_properties import api as desired_properties_api
from .system_info import api as system_info_api

api = Api(title="Api", version="1.0", description="Prototype")
api.add_namespace(max_threshold_api)
api.add_namespace(desired_properties_api)
api.add_namespace(system_info_api)

wrap = api.model('wrap', {
  "code": fields.Integer,
  "status": fields.String,
  "message": fields.String
})

@api.marshal_with(wrap)
@api.errorhandler(Exception)
def default_error_handler(error):
  return { 'code': 400, 'status': 'failure', 'message': str(error)}, 400