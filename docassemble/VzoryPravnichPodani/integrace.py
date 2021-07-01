import requests
from docassemble.base.util import get_config

def addEcomail (email, id, vzor):
  ecomailKey = get_config('ecomailKey')

  header = {'key': ecomailKey,'Content-Type': 'application/json'}

  values = '''
  {
  "subscriber_data": {
    "email": "'''+ email +'''",
    "tags": [
      "OBČAN 2.0",
      "'''+ vzor +'''",
      "Vzor"
    ]
  },
  "trigger_autoresponders": true,
  "update_existing": true,
  "resubscribe": true
  }
  '''
  r = requests.post('http://api2.ecomailapp.cz/lists/'+ id +'/subscribe', headers=header, data=values.encode('utf-8'))

  return
