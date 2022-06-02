from docassemble.base.util import validation_error
import requests
from bs4 import BeautifulSoup
import urllib
import json
import re
from docassemble.base.util import path_and_mimetype

def contains_spolek(x):
  x = x.lower()
  if "spolek" in x:
    return True
  elif "z.s." in x:
    return True
  elif "zapsaný spolek" in x:
    return True
  else:
    validation_error('Název spolku <strong>musí</strong> obsahovat "z.s.", "spolek", nebo "zapsaný spolek"')
  return

def string_pole(x):
  x = x.split('\r\n')
  return x

def obsahClanku(id):
  URL = 'https://frankbold.org/node/'+ id +'/'
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  polozky = soup.find('div', class_='content')
  return polozky

def query2dict(url):
    for polozka in url:
        print(polozka)
        try:
            url[polozka] = json.loads(urllib.parse.unquote_plus(url[polozka]).replace("'", '"'))
        except:
            continue
    return url

(obce_filename, obce_mimetype) = path_and_mimetype('data/static/obce.json')

def najitObec(obec, kraj):
    with open(obce_filename, encoding='utf-8') as d:
        data = json.load(d)
    for polozka in data["municipalities"]:
        if obec.lower() == polozka["hezkyNazev"].lower() and re.sub('(k|K)raj', '', kraj).strip().lower() == re.sub('(k|K)raj', '', polozka["adresaUradu"]["kraj"]).strip().lower():
            return(polozka)
    return(False)
