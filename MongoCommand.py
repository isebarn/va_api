import os
import pymongo
from bson.objectid import ObjectId
from pprint import pprint

def client():
  return pymongo.MongoClient(os.environ.get("DATABASE")
    .format(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))

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

  print(upsert_info)
  return upsert_info


'''
{
    _id: ObjectId('5f722a742930714468ed8929'),
    name: 'a',
    unique_id: 'u168380',
    os: {
        version: '6.2.9200.0',
        name: 'Microsoft Windows 10 Pro',
        locale: {
            geo_location: null,
            time_zone: 'IST',
            day_light_saving_support: false
        },
        culture: {
            name: 'en-US',
            LCID: '1033',
            language: 'English (United States)'
        },
        browser: [
            {
                name: 'IE',
                value: '9.11.17763.0' ieVersion
            },
            {
                name: 'Chrome',
                value: '84.0.4147.105' chromeVersion
            },
            {
                name: 'Firefox',
                value: 'Not Found' fireFoxVersion
            }
        ]
    },
    created_by: '',
    created_on: '',
    modified_by: '',
    modified_on: ISODate('2020-07-20T06:08:50.876Z')
}
'''