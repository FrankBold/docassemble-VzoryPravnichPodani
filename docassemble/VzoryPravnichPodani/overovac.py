# encoding: utf-8
from __future__ import unicode_literals
from docassemble.base.util import get_config

import requests
import json
import xmltodict

def overitUrad(dotaz, kriterium):
  URL = 'https://api.apitalks.store/ovm?filter={"where":{"'+ dotaz +'":"'+ kriterium +'"}}'
  headers = {'x-api-key': get_config('apitalksKey')}
  page = requests.get(URL, headers=headers)
  data = json.loads(page.text)
  vystup = data["data"][0]

  return(vystup)


def overitXml(ico):
  URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
  params = {'ico': ico}
  page = requests.get(URL, params=params)
  page.encoding = 'utf-8'
  ares_data = xmltodict.parse(page.text)
  response_root_wrapper = ares_data['are:Ares_odpovedi']
  response_root = response_root_wrapper['are:Odpoved']
  number_of_results = response_root['are:Pocet_zaznamu']

  if int(number_of_results) == 0:
        return "Nic jsme nenalezli."

  company_record = response_root['are:Zaznam']
  identification = company_record['are:Identifikace']
  address = identification['are:Adresa_ARES']

  info = {
    "firma": company_record.get('are:Obchodni_firma'),
    "ico": company_record.get('are:ICO'),
    "sidlo": address.get('dtt:Nazev_ulice') +" "+ address.get('dtt:Cislo_domovni') +"/"+ address.get('dtt:Cislo_orientacni') +", "+ address.get('dtt:PSC') +" "+ address.get('dtt:Nazev_obce')
  }

  return info
