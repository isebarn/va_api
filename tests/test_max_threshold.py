import json
from pytest import mark, raises
import queries.max_threshold

@mark.query_max_threshold_success
def test_query_max_threshold_success(app, client):
  res = client.get('/max_threshold/')
  assert res.status_code == 200

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 200
  assert result['status'] == 'success'

  assert 'Anonymize' in result['data']
  assert 'AutomationConfig' in result['data']
  assert 'AutomationInterval' in result['data']
  assert 'CPUThreshold' in result['data']
  assert 'DiskIOThreshold' in result['data']
  assert 'ImageCountThreshold' in result['data']
  assert 'LocalPath' in result['data']
  assert 'MemoryThreshold' in result['data']
  assert 'NetworkThreshold' in result['data']
  assert 'OCRinclusions' in result['data']
  assert 'PerfomanceInterval' in result['data']
  assert 'PollingInterval' in result['data']
  assert 'RemotePath' in result['data']
  assert 'SyncInterval' in result['data']
  assert 'inclusions' in result['data']
  assert 'initial_command' in result['data']
  assert 'isAutomationEnabled' in result['data']

@mark.query_max_threshold_failure
def test_query_max_threshold_failure(app, client, mocker):
  mocker.patch('queries.max_threshold.max_threshold', return_value=None)
  res = client.get('/max_threshold/')
  assert res.status_code == 400
  assert json.loads(res.data)['code'] == 400
  assert json.loads(res.data)['message'] == "No result"
  assert json.loads(res.data)['status'] == "failure"
