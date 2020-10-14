import os
import pymongo
from app_constants import databases

def client():
  return pymongo.MongoClient(os.environ.get("DATABASE")
    .format(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))

def get_collection(collection_name):
  collection = databases.get(collection_name, None)
  if collection is not None:
    return client()[collection.get('database')][collection.get('collection')]
