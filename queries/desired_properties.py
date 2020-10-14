from utils.DbConnection import get_collection
from bson.objectid import ObjectId

def desired_properties(device, user):
  # Item that will be returned
  result = {}

  # add sftp_config
  result['sftp_config'] = get_collection('sftp_settings').find_one({})

  # add device
  device = get_collection('devices').find_one({ 'name': device})
  if device == None:
    raise Exception('Device not found')

  result = {**result, **device}
  result['device_id'] = str(result['_id'])

  # fetch participant user
  participant = get_collection('participants').find_one({ 'name': user })
  if participant == None:
    raise Exception("Participant not found")

  # fetch from participant.va_info list, the item with
  # device_id that matches result['device_id']
  # and merge that with the result dict
  result = {**result, **next(filter(
    lambda x: str(x['device_id']) == result['device_id'], participant['va_info']), {})}


  # Add participants and convert inclusions to a string
  result = { **result, **participant}
  result['inclusions'] = ','.join(result['inclusions'])

  # Find the persona matching the participant and that users enabled applications
  persona = get_collection('personas').find_one({ '_id': ObjectId(participant['persona_id'])})
  enabled_applications = list(filter(lambda x: x['collect_data'] == True, persona['applications']))
  result['domains'] = []

  # every item in enabled applications needs substantial formatting before returning
  # NOTE: A lot of this might be unnecessary, depending on whether the pattern values are
  # unique or not
  for enabled_application in enabled_applications:
    data = {}
    data['automation_enabled'] = enabled_application.get('automation_enabled', True)
    data['capture_dom'] = enabled_application.get('capture_dom', True)

    # Get Applications.application to get domain
    application = get_collection('applications').find_one(
    { 'application_name_hash': enabled_application['application_name_hash']})
    data['domain'] = application['name']


    # iterate over data attributes of application_widget
    application_widgets = get_collection('persona_application_widgets').find(
      { "application_name_hash": enabled_application['application_name_hash']})
    data['data_field_groups'] = []
    data_group_dict = {}
    for application_widget in application_widgets:
      # get pattern keys and sort them to be able to group them
      pattern_keys = list(filter(lambda x: x.endswith('_pattern'), application_widget.keys()))
      pattern_keys.sort()

      # convert pattern values to a tuple
      group_tuple = tuple([application_widget[key] for key in pattern_keys])

      # add pattern values to data_group_dict
      # using call by reference to dictionary object, which might be confusing
      # NOTE: This may not be necessary, it depends on if there can be several
      # application_widgets with the same pattern in the db
      if group_tuple not in data_group_dict:

        # create new data_field_group,
        # it will have an id and a 'when' key that is unique
        data_field_group = {}
        data_field_group['id'] = len(data_group_dict) + 1
        data_field_group['when'] = { pattern_key: application_widget[pattern_key]
          for pattern_key in pattern_keys  }

      else:
        data_field_group = data_group_dict[group_tuple]

      # Add the data attributes to the data field group
      data_field_group['then'] = application_widget['data_attributes']

      # format the 'name' field in the 'then' group so that it is prepended by {11}
      for field_group in data_field_group['then']:
        field_group['name'] = "{{{}{}}}{}".format(
          1 if field_group['is_case_id'] else 0,
          1 if field_group['anonymise'] else 0,
          field_group['name'])

        # add data_field_group to the dictionary that stores it temporarily
        data_group_dict[group_tuple] = data_field_group


    for application_widget in data_group_dict.values():
      data['data_field_groups'].append(application_widget)

    result['domains'].append(data)

  return result
