# encoding: utf-8
from __future__ import unicode_literals
from docassemble.base.util import *

import requests
import json
import xmltodict
import datetime

def overitUrad(dotaz, kriterium):
  URL = 'https://api.apitalks.store/ovm?filter={"where":{"'+ dotaz +'":"'+ kriterium +'"}}'
  headers = {'x-api-key': get_config('apitalksKey')}
  page = requests.get(URL, headers=headers)
  data = json.loads(page.text)
  vystup = data["data"][0]

  return(vystup)

def uradDleDatovky(idds):
    xml = "<GetInfoRequest xmlns='http://seznam.gov.cz/ovm/ws/v1'><DataboxId>"+ idds +"</DataboxId></GetInfoRequest>"
    headers = {'Content-Type': 'application/xml'}

    data = requests.post('https://www.mojedatovaschranka.cz/sds/ws/call', data=xml, headers=headers)
    data.encoding = 'utf-8'
    return(xmltodict.parse(data.text)['GetInfoResponse']['Osoba'])

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
    }
  if address.get('dtt:Cislo_do_adresy') is None:
    if address.get('dtt:Cislo_orientacni') is None:
      info["sidlo"] = str(address.get('dtt:Nazev_ulice')) +" "+ str(address.get('dtt:Cislo_domovni')) +", "+ str(address.get('dtt:PSC')) +" "+ str(address.get('dtt:Nazev_obce'))
    else:
      info["sidlo"] = str(address.get('dtt:Nazev_ulice')) +" "+ str(address.get('dtt:Cislo_domovni')) +"/"+ str(address.get('dtt:Cislo_orientacni')) +", "+ str(address.get('dtt:PSC')) +" "+ str(address.get('dtt:Nazev_obce'))
  elif isinstance(address.get('dtt:Cislo_do_adresy'), str):
    info["sidlo"] = str(address.get('dtt:Nazev_ulice')) +" "+ str(address.get('dtt:Cislo_do_adresy')) +", "+ str(address.get('dtt:PSC')) +" "+ str(address.get('dtt:Nazev_obce'))
  else:
    info["sidlo"] = str(address.get('dtt:Nazev_ulice')) +", "+ str(address.get('dtt:PSC')) +" "+ str(address.get('dtt:Nazev_obce'))
  
  return info

def getholidays(year):

    holidays = {
                (1, 1),   #Novy rok
                (1, 5),   #Svatek prace
                (8, 5),   #Den vitezstvi
                (5, 7),   #Cyril a Metodej
                (6, 7),   #Jan Hus
                (28, 9),  #Den Ceske statnosti
                (28, 10), #Vznik CS statu
                (17, 11), #Den boje za svobodu a dem.
                (24, 12), #Stedry den
                (25, 12), #1. svatek Vanocni
                (26, 12), #2. svatek Vanocni
               }

    # Easter holiday LUT source http://www.whyeaster.com/customs/dateofeaster.shtml
    easterlut = [(4, 14), (4, 3), (3, 23), (4, 11), (3, 31), (4, 18), (4, 8),
                 (3, 28), (4, 16), (4, 5), (3, 25), (4, 13), (4, 2), (3, 22),
                 (4, 10), (3, 30), (4, 17), (4, 7), (3, 27)]
    easterday = datetime.date(year, *easterlut[year%19])
    easterday += datetime.timedelta(6 - easterday.weekday())
    # print("Easter Sunday is on ", easterday)
    holidays.update(((d.day, d.month) for d in [easterday - datetime.timedelta(2),
                                                easterday + datetime.timedelta(1)]))
    return holidays

def isholiday(date):
    svatek = (date.day, date.month) in getholidays(date.year)
    return svatek == True or date.weekday() >= 5

def lhutaOverit(lhuta,datum):
  datum = datetime.date(int(format_date(datum,format='yyyy')),int(format_date(datum,format='M')),int(format_date(datum,format='d')))
  konecLhuty = datum + datetime.timedelta(lhuta)
  while isholiday(konecLhuty) == True:
    konecLhuty += datetime.timedelta(1)
    lhuta += 1
  rozdil = datetime.date.today() - datum
  if rozdil.days <= lhuta:
    return True, konecLhuty
  else:
    return False, konecLhuty
