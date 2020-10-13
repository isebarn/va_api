from flask_restx import Namespace, Resource, fields
from flask import abort
import queries.max_threshold

api = Namespace("max_threshold", description="Configuration")

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

success = api.model('success', {
  "code": fields.Integer,
  "status": fields.String,
  "data": fields.Nested(model),
})

@api.route("/")
class MaxThresholdClass(Resource):
  @api.marshal_with(success)
  def get(self):
    max_threshold = queries.max_threshold.max_threshold()
    print(max_threshold)
    if max_threshold == None:
      raise Exception("No result")

    return { 'code': 200, 'status': 'success', 'data': max_threshold}