from utils.DbConnection import get_collection

def get():
  return get_collection('va_preference').find_one({})
