from flask_restx import Namespace, Resource, fields
from flask import abort
from MongoQuery import va_max_threshold

api = Namespace("max_threshold", description="Configuration")

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



model = api.model('Model', {
  'initial_command': fields.String,
  'inclusions': fields.String(attribute='configs.inclusions'),
  'isAutomationEnabled': fields.String(attribute='configs.is_automation_enabled', default='false'),
  'OCRinclusions': fields.String(attribute='configs.ocr_inclusions'),
  'AutomationConfig': fields.String(attribute='configs.automation'),
  'DiskIOThreshold': fields.Integer(attribute='data_sync_thresholds.disk_i/o'),
  'MemoryThreshold': fields.Integer(attribute='data_sync_thresholds.memory'),
  'NetworkThreshold': fields.Integer(attribute='data_sync_thresholds.network'),
  'ImageCountThreshold': fields.Integer(attribute='data_sync_thresholds.image_count'),
  'LocalPath': fields.String(attribute='path.local'),
  'RemotePath': fields.String(attribute='path.remote'),
  'PerfomanceInterval': fields.Integer(attribute='intervals.performance'),
  'SyncInterval': fields.Integer(attribute='intervals.sync'),
  'AutomationInterval': fields.Integer(attribute='intervals.automation'),
  'CPUThreshold': fields.Integer(attribute='intervals.cpu'),
  'PollingInterval': fields.Integer(attribute='intervals.polling'),
  "Anonymize": fields.String(attribute='configs.anonymize')
})

@api.route("/")
class MaxThresholdClass(Resource):

  @api.marshal_with(model, envelope='data')
  def get(self):
    max_threshold = va_max_threshold()

    if max_threshold == None:
      raise QueryError("No result")

    return max_threshold