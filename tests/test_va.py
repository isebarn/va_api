import json
from pytest import mark, raises
import queries.va

@mark.query_va_success
def test_query_va_success(app, client):
  res = client.get('/va/')
  assert res.status_code == 200

  result = json.loads(res.get_data())
  assert isinstance(result, dict)
  assert result['code'] == 200
  assert result['status'] == 'success'


@mark.query_va_failure
def test_query_va_failure(app, client, mocker):
  pass
  mocker.patch('queries.va.get', return_value=None)
  res = client.get('/va/')
  assert res.status_code == 400
  assert json.loads(res.data)['code'] == 400
  assert json.loads(res.data)['message'] == "No result"
  assert json.loads(res.data)['status'] == "failure"
