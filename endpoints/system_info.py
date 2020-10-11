from flask_restx import Namespace, Resource, fields
from flask import abort
from flask_restx import reqparse
from MongoCommand import system_info as save_system_info

api = Namespace("system_info", description="System Info")

success_wrap = api.model('success_data', {
  'n': fields.Integer,
  'nModified': fields.Integer,
  'ok': fields.Integer,
  'updatedExisting': fields.Boolean
})

success = api.model('success', {
  "code": fields.Integer,
  "status": fields.String,
  "data": fields.Nested(success_wrap),
})

system_info = api.model('system_info', {
  '_id': fields.String(default=None),
  'osVersion': fields.String(required=True),
  'language': fields.String(required=True),
  'cultureName': fields.String(required=True),
  'cultureLCID': fields.String(required=True),
  'geoLocation': fields.String(required=True),
  'ieVersion': fields.String(defailt=None),
  'chromeVersion': fields.String(defailt=None),
  'fireFoxVersion': fields.String(defailt=None),
  'device': fields.String(required=True)
})

def validate_post(payload):
  required = [x[0] for x in system_info.items() if x[1].required]
  missing_required = next(filter(lambda x: x not in payload, required), None)

  # check for missing fields
  if missing_required != None:
    raise Exception("Required field missing: {}".format(missing_required))

  if any([not isinstance(v, str) for k,v in payload.items()]):
    raise Exception("All fields should be string values")

@api.route("/")
class SystemInfoClass(Resource):
  @api.expect(system_info, validate=False)
  @api.marshal_with(success)
  def post(self):

    # validation must be done manually, because otherwise we cannot wrap the error
    validate_post(api.payload)

    return { 'code': 200, 'status': 'success', 'data': save_system_info(api.payload)}
