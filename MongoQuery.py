import os
import pymongo

def client():
  return pymongo.MongoClient(os.environ.get("DATABASE").format(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))

def va_max_threshold():
  db = client()[os.environ.get('DB')]
  return db.va_preference.find_one({})
