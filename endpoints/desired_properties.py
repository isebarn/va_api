from flask_restx import Namespace, Resource, fields
from flask import abort
from flask_restx import reqparse
import queries.desired_properties

api = Namespace("desired_properties", description="Desired Properties")

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
  'anonymise': fields.Boolean,
  'is_case_id': fields.Boolean,
  'w_path': fields.String,
  'name': fields.String,
  'property_ids': fields.List(fields.String(lambda x: str(x))),
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

success = api.model('success', {
  "code": fields.Integer,
  "status": fields.String,
  "data": fields.Nested(model),
})


parser = reqparse.RequestParser()
parser.add_argument('device', type=str, help='Device name')
parser.add_argument('user', type=str, help='User name')

@api.route("/")
class DesiredPropertiesClass(Resource):
  @api.marshal_with(success)
  def get(self):
    args = parser.parse_args()

    if args.device == None:
      raise Exception("Device name missing required parameter")

    if args.user == None:
      raise Exception("User name missing required parameter")
    result = queries.desired_properties.desired_properties(args.device, args.user)

    if result == None:
      raise QueryError("No result")

    return { 'code': 200, 'status': 'success', 'data': result}
