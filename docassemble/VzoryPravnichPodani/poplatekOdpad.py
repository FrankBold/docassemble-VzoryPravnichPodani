import csv
import re
import json
import requests
import io
import docx
import textract
import tempfile
from docassemble.base.util import path_and_mimetype, ocr_file, DAObject, DAFile

(filename, mimetype) = path_and_mimetype('data/static/obce.json')

def najitObec(obec, kraj):
    with open(filename, encoding='utf-8') as d:
        data = json.load(d)
    for polozka in data["municipalities"]:
        if obec.lower() == polozka["hezkyNazev"].lower() and re.sub('(k|K)raj', '', kraj).strip().lower() == re.sub('(k|K)raj', '', polozka["adresaUradu"]["kraj"]).strip().lower():
            return(polozka)
    return(False)

def vyhlaskyObce(idds):
    with requests.Session() as s:
        r = s.get('https://sbirkapp.gov.cz/vyhledavani/vysledek?typ=ozv&ovm='+idds+'&kod_vusc=&ucinnost_od=&ucinnost_do=&oblast=&zmocneni=&nazev=&znacka=&format_exportu=csv')
        r = r.content.decode('utf-8')

        r = csv.DictReader(r.splitlines())

        vyhlasky = []

        for radek in r:
            vyhlasky.append(radek)

        return(vyhlasky)

def vyhlaskaText(id):
    r = requests.get('https://sbirkapp.gov.cz/detail/'+id+'/text')
    if "pdf" in r.headers['content-type']:
      thefile = DAFile("thefile")
      thefile.initialize(filename="vyhlaska.pdf", extension="pdf")
      thefile.write(r.content, binary="true")
      return(ocr_file(thefile, language="cs"))
    elif "docx" in r.headers['content-type']:
      obsah = []
      doc = docx.Document(io.BytesIO(r.content))
      for para in doc.paragraphs:
        obsah.append(para.text)
      return('\n'.join(obsah))
    elif "doc" == r.headers['content-type'] or "application/msword" == r.headers['content-type']:
      r = requests.post('https://hook.integromat.com/7nmnpym8m6g0byshhd2d7e6jh6y8gcjn?url=https://sbirkapp.gov.cz/detail/'+id+'/text')
      text = r.content.decode('utf-8')
      return(text)
    elif "odt" in r.headers['content-type']:
      try:
        with tempfile.NamedTemporaryFile() as tmp:
          r = requests.get('https://sbirkapp.gov.cz/detail/'+id+'/text')
          tmp.write(r.content)
          text = textract.process(tmp.name, extension='odt').decode('utf-8')
          return(text)
      except Exception as e:
          return(e)
    else:
      return(r.headers['content-type'])

def typPoplatku(text):
    text = text[:800]
    if "místním poplatku" not in text:
        return [False,"Vyhláška se zřejmě nezabývá poplatkem za komunální odpad."]
    else:
        if "za odkládání komunálního odpadu" in text and "obecní systém odpadového hospodářství" in text:
            return [False,"Obojí..."]
        elif "za odkládání komunálního odpadu" in text:
            return [True,"znemovitosti"]
        elif "systém odpadového hospodářství" in text:
            return [True,"system"]
        else:
            return [False,"Ani jedno"]
