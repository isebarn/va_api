from flask_restx import Namespace, Resource, fields, marshal
import queries.va
import json

api = Namespace("va", description="Root path")

os = api.model('os', {
  'OSVersion': fields.String(attribute='os.version'),
  'OSName': fields.String(attribute='os.name'),
  'Language': fields.String(attribute='os.culture.language'),
  'CultureName': fields.String(attribute='os.culture.name'),
  'CultureLCID': fields.String(attribute='os.culture.LCID'),
  'GeoLocation': fields.String(attribute='os.locale.geo_location'),
  'IEVersion': fields.String(attribute=lambda x: 
    next(filter(
      lambda y: y['name'] == 'IE', x['os']['browser']))['value']),
  'ChromeVersion': fields.String(attribute=lambda x: 
    next(filter(
      lambda y: y['name'] == 'Chrome', x['os']['browser']))['value']),
  'FireFoxVersion': fields.String(attribute=lambda x: 
    next(filter(
      lambda y: y['name'] == 'Firefox', x['os']['browser']))['value']),
  'UserNameHash': fields.String(attribute='participants.participant_name_hash'),
  'TimeZoneStandardName': fields.String(attribute='os.locale.time_zone'),
  'SupportsDaylightSavingTime': fields.String(attribute='os.locale.day_light_saving_support'),
  #'ProductVersion': fields.String(attribute='participants.va_info.version'),
})

model = api.model('Model', {
  'id': fields.String(attribute=lambda x: str(x['_id'])),
  'command': fields.String(attribute='participants.command'),
  'device': fields.String(attribute='name'),
  'user': fields.String(attribute='participants.name'),
  #'va_status': fields.String(attribute='participants.va_info.status'),
  'last_connection_time': fields.String(attribute='participants.va_info.last_seen_on'),
  'last_activity_processed': fields.DateTime(
    attribute=lambda x: x['participants']['last_activity_processed_on'].as_datetime()),
  'is_assigned': fields.Boolean(
    attribute=lambda x: x['participants']['persona_id'] != None),
  #'process_name': fields.String(attribute=''),
  #'user_alias': fields.String(attribute=''),
  'name_hash': fields.String(attribute='participants.participant_name_hash'),
  'va_last_updated_time': fields.DateTime(
    attribute=lambda x: x['participants']['modified_on'].as_datetime()),
})

model['system_info'] = os

'''
modell = {}
modell["id"] = fields.String(attribute=lambda x: str(x["_id"]))
modell["system_info"] = {}
modell["system_info"]["OSVersion"] = fields.String(attribute=lambda x: str(x['participants']["_id"]))
'''

success = api.model('success', {
  "code": fields.Integer,
  "status": fields.String,
  "data": fields.List(fields.Nested(model)),
})

'''
    [
      {
      "system_info": {
        "UserNameHash": "a1ec163b050a9fca49d102a541fb26aa",
      }, // devices collection
      "process_name": "Same Participant Multiple Machines", // from persona_id of participants collection
      "user_alias": "", // generated via code based on anonymize
      }
    ]
'''





@api.route("/")
class VAClass(Resource):
  @api.marshal_with(success)
  def get(self):
    result = queries.va.get()

    if result == None:
      raise Exception("No result")

    return { 'code': 200, 'status': 'success', 'data': result[0:1] }
