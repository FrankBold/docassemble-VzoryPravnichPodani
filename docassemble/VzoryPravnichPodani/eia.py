import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re
import json
import locale

obsah = [[["Kód záměru:","s","kod"],["Název záměru:","s","nazev"],["Znění novely zákona:","s","novela"],["Stav:","s","stav"],["Zařazení:","a","zarazeni"],["Umístění:","t","lokalita"],["Příslušný úřad:","s","urad"],["Datum a čas posledních úprav:","d","aktualizovano"],["Oznamovatel:","s","oznamovatel"],["IČO oznamovatele:","l","ic"]],[["Vliv na soustavu Natura 2000:","s","natura"],["Datum zveřejnění informace o oznámení na úřední desce dotčeného kraje:","d","datum"],["Termín pro zaslání vyjádření:","d","vyjadreniTermin"],["Zpracovatel oznámení:","l","zpracovatel"],["Text oznámení záměru:","f","text"],["Informace o oznámení:","f","info"]],[["Datum zveřejnění závěrů zjišťovacího řízení na úřední desce dotčeného kraje:","d","zverejneno"],["Závěry zjišťovacího řízení:","f","zaver"],["Informace o závěru zjišťovacího řízení:","f","info"],["Vliv na soustavu Natura 2000:","s","natura"]],[["Zpracovatel dokumentace:","l","zpracovatel"],["Zpracovatel - soustava Natura 2000:","l","zpracovatelNatura"],["Datum zveřejnění informace o dokumentaci na úřední desce dotčeného kraje:","d","zverejneno"],["Termín pro zaslání vyjádření:","d","vyjadreniTermin"],["Text dokumentace:","f","text"],["Text přepracované/doplněné dokumentace:","f","doplneni"],["Informace o dokumentaci:","f","info"],["Vrácení dokumentace:","f","vraceno"]],[["Zpracovatel posudku:","l","zpracovatel"],["Posuzovatel - soustava Natura 2000:","l","zpracovatelNatura"],["Datum zveřejnění informace o posudku na úřední desce dotčeného kraje:","d","zverejneno"],["Termín pro zaslání vyjádření:","d","vyjadreniTermin"],["Text posudku:","f","text"],["Informace o posudku:","f","info"]],[["Datum zveřejnění informace o veřejném projednání na úřední desce dotčeného kraje:","d","zverejneno"],["Informace o místě a času konání 1. veřejného projednání:","f","info"],["Zápis z 1. veřejného projednání:","f","zapis"]],[["Datum zveřejnění stanoviska na úřední desce dotčeného kraje:","d","zverejneno"],["Stanovisko:","s","stanovisko"],["Významný negativní vliv na soustavu Natura 2000:","s","natura"],["Text stanoviska:","f","text"],["Prodloužení stanoviska:","f","prodlouzeno"]]]

kat = ["uvod","oznameni","zjistovaci rizeni", "dokumentace", "posudek", "projednani", "stanovisko"]

export = []

locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

def detailEIA(kod):
    vystup = {"uvod": {},"oznameni": {},"zjistovaci rizeni": {}, "dokumentace": {}, "posudek": {}, "projednani": {}, "stanovisko": {}}
    subpage = requests.get('https://portal.cenia.cz/eiasea/detail/EIA_'+ kod)
    subsoup = BeautifulSoup(subpage.content, 'html.parser')
    tabulka = subsoup.find_all("table")
    tabulka = str(tabulka[1]).replace("<br/>", " ")

    casti = re.split('<tr>\n\t*<td colspan="2".+?>.*?</td>\n\t*</tr>', tabulka)

    i = 0
    for kus in casti:
        cast = BeautifulSoup(kus, 'html.parser')
        for sekce in obsah[i]:
            subtd = cast.find('td', class_='label', text=sekce[0])
            next = subtd.next_sibling.next_sibling
            if sekce[1] == "s": # Pokud jde o string, jen jen propíšeme
                vystup[kat[i]][sekce[2]] = next.text
            elif sekce[1] == "d": # Pokud jde o datum, převedeme ho do standardního formátu
                if next.text:
                    vystup[kat[i]][sekce[2]] = str(datetime.strptime(re.sub('CE(S)*T', '', subtd.next_sibling.next_sibling.text), '%a %b %d %H:%M:%S %Y').strftime("%d. %m. %Y"))
                else:
                    vystup[kat[i]][sekce[2]] = None
            elif sekce[1] == "t": # Tabulku převedeme do dict.
                tabulka = next.find('table')
                if tabulka is not None:
                    lokality = tabulka.find_all('tr')
                    misto = []
                    for lokalita in lokality[1::]:
                        udaje = lokalita.find_all('td')
                        misto.append({'kraj': udaje[0].text, 'okres': udaje[1].text, 'obec': udaje[2].text,'katastr': udaje[3].text})
                    vystup[kat[i]][sekce[2]] = misto
            elif sekce[1] == "l": # Odkaz převedeme do dict
                if next.text and next.text.replace("\n",""):
                    if next.a['href'].startswith("http"):
                        odkaz = {'label': next.text.replace("\n",""), 'link': next.a['href']}
                    else:
                        odkaz = {'label': next.text.replace("\n",""), 'link': 'https://portal.cenia.cz'+ next.a['href']}
                    vystup[kat[i]][sekce[2]] = odkaz
                else:
                    vystup[kat[i]][sekce[2]] = None
            elif sekce[1] == "a": # Text s více položkami převedeme na pole
                vystup[kat[i]][sekce[2]] = next.text.split(";")
            elif sekce[1] == "f": # Soubor převedeme do dict
                soubor = []
                if next.text and len(next.find_all("a")) == 1:
                    datum = next.text.split(" - ")[1]
                    if next.a['href'].startswith("http"):
                        soubor.append({'label': next.text.split(" (")[0], 'link': next.a['href'], 'zverejneno': str(datetime.strptime(datum.strip(), '%d.%m.%Y %H:%M:%S'))})
                    else:
                        soubor.append({'label': next.text.split(" (")[0], 'link': 'https://portal.cenia.cz'+next.a['href'], 'zverejneno': str(datetime.strptime(datum.strip(), '%d.%m.%Y %H:%M:%S'))})
                    vystup[kat[i]][sekce[2]] = soubor
                elif next.text and len(next.find_all("a")) > 1:
                    souborCast = re.sub('<\/*td.*?>', '', str(next))
                    souborCast = re.split('(<a.*?:\d{2} )', souborCast)
                    for souborPolozka in souborCast[1::2]:
                        if re.search('href="(.*?)"', souborPolozka).group(1).startswith("http"):
                            soubor.append({'label': re.search('>(.+?)</a>', souborPolozka).group(1), 'link': re.search('href="(.*?)"', souborPolozka).group(1), 'zverejneno': str(datetime.strptime(re.search('- (.+) $', souborPolozka).group(1), '%d.%m.%Y %H:%M:%S'))})
                        else:
                            soubor.append({'label': re.search('>(.+?)</a>', souborPolozka).group(1), 'link': 'https://portal.cenia.cz'+re.search('href="(.*?)"', souborPolozka).group(1), 'zverejneno': str(datetime.strptime(re.search('- (.+) $', souborPolozka).group(1), '%d.%m.%Y %H:%M:%S'))})
                    vystup[kat[i]][sekce[2]] = soubor
                else:
                    vystup[kat[i]][sekce[2]] = None
        if i == 6:
            break
        i+=1

    return vystup