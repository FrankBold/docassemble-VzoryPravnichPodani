import csv
from docassemble.base.util import path_and_mimetype

(filename, mimetype) = path_and_mimetype('data/static/obyvatele_full.csv')

__all__ = ['pocetObyvatel']

def pocetObyvatel(obec):
  vysledek = []
  with open(filename, newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile, delimiter=';')
      for row in reader:
          if row[1] == obec:
              vysledek.append(row)

  return(vysledek)
