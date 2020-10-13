from utils.DbConnection import client

def system_info(system_info):
  upsert_info = client()['Users']['devices'].update({'name': system_info['device']},
    {'$set':
      {
        'os.version': system_info.get('osVersion'),
        'os.locale.geo_location': system_info.get('geoLocation'),
        'os.culture.name': system_info.get('cultureName'),
        'os.culture.LCID': system_info.get('cultureLCID'),
        'os.culture.language': system_info.get('language'),
        'os.browser': [
          { 'name': 'IE', 'value': system_info.get('ieVersion', None)},
          { 'name': 'Chrome', 'value': system_info.get('chromeVersion', None)},
          { 'name': 'Firefox', 'value': system_info.get('fireFoxVersion', None)}
        ]
      }
    },
    upsert=True,
    multi=False)

  return upsert_info
