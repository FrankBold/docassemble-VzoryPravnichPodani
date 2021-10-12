import requests
from docassemble.base.util import get_config
import json

ecomailKey = get_config('ecomailKey')

def detailEcomail (email):
    header = {'key': ecomailKey,'Content-Type': 'application/json'}
    r = requests.get('https://api2.ecomailapp.cz/subscribers/'+email, headers=header)
    return r.json()

def addEcomail (email, id, vzor):


  header = {'key': ecomailKey,'Content-Type': 'application/json'}

  contact = detailEcomail(email)
  if "tags" in contact:
    tagy = contact["subscriber"]["tags"]
  else:
    tagy = []

  tagy.append("OBČAN 2.0")
  tagy.append("Vzor")

  values = {}
  values["subscriber_data"] = {}
  values["subscriber_data"]["email"] = email
  values["subscriber_data"]["tags"] = list(set(tagy))
  values["trigger_autoresponders"] = True
  values["update_existing"] = True
  values["resubscribe"] = True

  r = requests.post('http://api2.ecomailapp.cz/lists/'+ id +'/subscribe', headers=header, data=json.dumps(values))
  return r.json()

def hs_smlouva(idSmlouvy):
    header = {"Authorization": "Token "+get_config('HlidacStatuKey')}
    url = "https://www.hlidacstatu.cz/Api/v2/Smlouvy/"+idSmlouvy
    r = requests.get(url, headers=header)
    return r.json()
