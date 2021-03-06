from docassemble.base.util import validation_error
import requests
from bs4 import BeautifulSoup

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