from utils.DbConnection import client

def max_threshold():
  return client().Users.va_preference.find_one({})
