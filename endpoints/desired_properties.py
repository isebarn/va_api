from flask_restx import Namespace, Resource, fields
from flask import abort
from flask_restx import reqparse
from MongoQuery import va_desired_properties

api = Namespace("desired_properties", description="Desired Properties")

class QueryError(Exception):
  def __init__(self, message):
    self.response = { 'data': message }
    self.code = 500
    self.status = "failure"
    self.message = ""

error_fields = api.model('error', {
  "response": fields.String,
  "message": fields.String,
  "status": fields.String,
  "code": fields.Integer
})

@api.errorhandler(QueryError)
@api.marshal_with(error_fields, code=400)
@api.errorhandler
def default_error_handler(error):
  '''Default error handler'''
  return error

parser = reqparse.RequestParser()
parser.add_argument('device', type=str, help='Device name')
parser.add_argument('user', type=str, help='User name')

sftp_config = api.model('sftp', {
  'username': fields.String,
  'password': fields.String,
  'host_address': fields.String,
  'has_private_key': fields.String,
  'private_key': fields.String
})


when = api.model('when', {
  'agent_type_pattern': fields.String,
  'control_id_pattern': fields.String,
  'event_path_pattern': fields.String,
  'title_pattern': fields.String,
  'url_pattern': fields.String,
})

query = api.model('query', {
  'property_type': fields.Integer,
  'property_value': fields.Raw
})

then = api.model('then', {
  'anonymize': fields.Boolean,
  'is_case_id': fields.Boolean,
  'w_path': fields.String,
  'name': fields.String,
  'propertyIDs': fields.String,
  'query': fields.List(fields.Nested(query))
})

data_field_group = api.model('data_field_group', {
  'id': fields.Integer,
  'when': fields.Nested(when),
  'then': fields.List(fields.Nested(then))
})

domains = api.model('domains', {
  'domain': fields.String,
  'automation_enabled': fields.Boolean,
  'capture_dom': fields.Boolean,
  'data_field_groups': fields.List(fields.Nested(data_field_group))
})


model = api.model('Model', {
  'sftp_config': fields.Nested(sftp_config),
  'domains': fields.List(fields.Nested(domains)),
  'device_id': fields.String,
  'command': fields.String,
  'SkanAutomationDllPath': fields.String(default=""),
  'ListenerExePath': fields.String(default=""),
  'LatestVaBuildNumber': fields.String(attribute='latest_va_build_number'),
  'LatestVaVersion': fields.String(attribute='latest_va_version'),
  'UpdateDll': fields.Boolean(default=False),
  'UpdateExe': fields.Boolean(default=False),
  'inclusions': fields.String,
  'remote_path': fields.String,
  'last_updated_time': fields.String(attribute='modified_on'),
  'AutomationConfig': fields.String(attribute='automation_config'),
})

@api.route("/")
class DesiredPropertiesClass(Resource):

  @api.marshal_with(model)
  def get(self):
    args = parser.parse_args()

    desired_properties = va_desired_properties(args.device, args.user)

    if desired_properties == None:
      raise QueryError("No result")

    return desired_properties