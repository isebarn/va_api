import os
import pymongo

def client():
  return pymongo.MongoClient(os.environ.get("DATABASE")
    .format(os.environ.get("USERNAME"), os.environ.get("PASSWORD")))
