import json
from pytest import mark, raises
import json
from datetime import datetime

def load_file(file):
  with open(file) as f:
    return json.load(f)


@mark.post_system_info_failure
def test_post_system_info_fail_missing_cultureLCID(app, client):
  data = load_file('./tests/testdata/system_info_missing_cultureLCID.json')
  res = client.post('/system_info/', json=data)
  result = json.loads(res.get_data())

  assert res.status_code == 400
  assert result['message'] == "Required field missing: cultureLCID"
  assert result['status'] == "failure"

@mark.post_system_info_failure
def test_post_system_info_fail_missing_cultureName(app, client):
  data = load_file('./tests/testdata/system_info_missing_cultureName.json')
  res = client.post('/system_info/', json=data)

  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert result['message'] == "Required field missing: cultureName"
  assert result['status'] == "failure"

@mark.post_system_info_failure
def test_post_system_info_fail_missing_geoLocation(app, client):
  data = load_file('./tests/testdata/system_info_missing_geoLocation.json')
  res = client.post('/system_info/', json=data)

  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert result['message'] == "Required field missing: geoLocation"
  assert result['status'] == "failure"

@mark.post_system_info_failure
def test_post_system_info_fail_missing_language(app, client):
  data = load_file('./tests/testdata/system_info_missing_language.json')
  res = client.post('/system_info/', json=data)

  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert result['message'] == "Required field missing: language"
  assert result['status'] == "failure"

@mark.post_system_info_failure
def test_post_system_info_fail_missing_osVersion(app, client):
  data = load_file('./tests/testdata/system_info_missing_osVersion.json')
  res = client.post('/system_info/', json=data)

  assert res.status_code == 400

  result = json.loads(res.get_data())
  assert result['message'] == "Required field missing: osVersion"
  assert result['status'] == "failure"


@mark.post_system_info_success
def test_post_system_info_success_insert(app, client):
  data = load_file('./tests/testdata/system_info_successful_1.json')
  date = datetime.now()
  data['chromeVersion'] = "{}.{}.{}.{}.{}.{}".format(
    date.year, date.month, date.day, date.hour, date.minute, date.second)
  data['device'] = data['chromeVersion'].replace('.', '')

  res = client.post('/system_info/', json=data)
  assert res.status_code == 200

  result = json.loads(res.get_data())
  assert res.status_code == 200
  assert result['status'] == 'success'

  assert result['data']['n'] == 1
  assert result['data']['nModified'] == 0
  assert result['data']['ok'] == 1
  assert result['data']['updatedExisting'] == False

@mark.post_system_info_success
def test_post_system_info_success_update(app, client):
  # First set the data in the db
  data = load_file('./tests/testdata/system_info_successful_1.json')
  res = client.post('/system_info/', json=data)
  assert res.status_code == 200

  # Now the real test begins
  # Get dataset 1 and save
  data = load_file('./tests/testdata/system_info_successful_1.json')
  res = client.post('/system_info/', json=data)
  result = json.loads(res.get_data())
  assert res.status_code == 200

  assert result['code'] == 200
  assert result['status'] == 'success'

  assert result['data']['n'] == 1
  assert result['data']['nModified'] == 0
  assert result['data']['ok'] == 1
  assert result['data']['updatedExisting'] == True

  # Now the real test begins
  # Get dataset 2 and save
  data = load_file('./tests/testdata/system_info_successful_2.json')
  res = client.post('/system_info/', json=data)
  result = json.loads(res.get_data())
  assert res.status_code == 200

  assert result['code'] == 200
  assert result['status'] == 'success'

  assert result['data']['n'] == 1
  assert result['data']['nModified'] == 1
  assert result['data']['ok'] == 1
  assert result['data']['updatedExisting'] == True
