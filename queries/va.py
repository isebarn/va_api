from utils.DbConnection import get_collection

def get():
  return list(get_collection('devices').aggregate(
    [
      { "$lookup":
        {
          "from": "participants",
          "pipeline":
          [
              { "$match": { "$expr": { "$in": ["$_id", "$va_info.device_id"] }}},
          ],
          "as": "participants"
      }},
      { "$unwind": "$participants" }
    ]))