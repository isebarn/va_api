import json
from pytest import mark, raises
from MongoQuery import va_max_threshold

'''
missing username
missing device name
username w. no user empty result set
unknown device empty result set
'''
@mark.query_desired_properties_success
def test_query_desired_properties(app, client):
  res = client.get('/desired_properties/?user=BOMW0000029528&device=a')
  assert res.status_code == 200

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 200
  assert result['status'] == 'success'
  assert isinstance(result['data'], dict)

@mark.query_desired_properties_failure
def test_query_desired_properties_device_not_found(app, client):
  res = client.get('/desired_properties/?user=BOMW0000029528&device=ab')
  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 400
  assert result['status'] == 'failure'
  assert result['message'] == 'Device not found'

@mark.query_desired_properties_failure
def test_query_desired_properties_participant_not_found(app, client):
  res = client.get('/desired_properties/?user=BO0MW0000029528&device=a')
  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 400
  assert result['status'] == 'failure'
  assert result['message'] == 'Participant not found'

@mark.query_desired_properties_failure
def test_query_desired_properties_missing_device(app, client):
  res = client.get('/desired_properties/?user=BO0MW0000029528')
  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 400
  assert result['status'] == 'failure'
  assert result['message'] == 'Device name missing required parameter'

@mark.query_desired_properties_failure
def test_query_desired_properties_missing_participant(app, client):
  res = client.get('/desired_properties/?device=a')
  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 400
  assert result['status'] == 'failure'
  assert result['message'] == 'User name missing required parameter'

