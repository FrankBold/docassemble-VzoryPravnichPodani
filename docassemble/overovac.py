# encoding: utf-8
from __future__ import unicode_literals

import logging
import re
import sys
import warnings

import requests
import xmltodict
from bs4 import BeautifulSoup

def overit(ico, firma):
  URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
  params = {'ico': ico, 'obchodni_firma': firma}
  page = requests.get(URL, params=params)
  page.encoding = 'utf-8'
  soup = BeautifulSoup(page.content, 'xml')
  if soup.find('are:Pocet_zaznamu').string == "0":
    return "Nebyla nalezena žádná shoda."
  elif soup.find('are:Pocet_zaznamu').string == "1":
    info = {
      "firma": soup.find('are:Obchodni_firma').string,
      "ico": soup.find('are:ICO').string,
      "sidlo": soup.find('dtt:Nazev_ulice').string +" "+ soup.find('dtt:Cislo_domovni').string +"/"+ soup.find('dtt:Cislo_orientacni').string +", "+ soup.find('dtt:PSC').string +" "+ soup.find('dtt:Nazev_obce').string
    }
    return info
  else:
    pole = []
    firmy = soup.find_all('are:Obchodni_firma')
    for polozka in firmy:
      pole.append(repr(polozka.string).strip("'"))
    return pole

def overitXml(ico, firma):
  URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
  params = {'ico': ico, 'obchodni_firma': firma}
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