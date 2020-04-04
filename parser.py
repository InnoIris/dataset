from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import os.path

folder = 'train/'
instruments = ['hammer']

with open('labels_train.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for instrument in instruments:
    directory_name = os.path.join(folder, instrument)
    for filename in os.listdir(directory_name):
      label = instrument
      filename_jpg = filename[:-4] + '.jpg'
      filename_xml = filename[:-4] + '.xml'
      handler = None
      try:
        handler = open(os.path.join(directory_name, filename_xml)).read()
      except:
        print("Could not find", filename_xml)
        continue
      filename_str = os.path.join(directory_name, filename_jpg)
      soup = BeautifulSoup(handler, "xml")
      xmin = int(soup.xmin.string)
      xmax = int(soup.xmax.string)
      ymin = int(soup.ymin.string)
      ymax = int(soup.ymax.string)
      row = [filename_str, xmin, xmax, ymin, ymax, instruments.index(instrument)]
      writer.writerow(row)

folder = 'validation/'

with open('labels_val.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for instrument in instruments:
    directory_name = os.path.join(folder, instrument)
    for filename in os.listdir(directory_name):
      label = instrument
      filename_jpg = filename[:-4] + '.jpg'
      filename_xml = filename[:-4] + '.xml'
      handler = None
      try:
        handler = open(os.path.join(directory_name, filename_xml)).read()
      except:
        print("Could not find", filename_xml)
        continue
      filename_str = os.path.join(directory_name, filename_jpg)
      soup = BeautifulSoup(handler, "xml")
      xmin = int(soup.xmin.string)
      xmax = int(soup.xmax.string)
      ymin = int(soup.ymin.string)
      ymax = int(soup.ymax.string)
      row = [filename_str, xmin, xmax, ymin, ymax, instruments.index(instrument)]
      writer.writerow(row)
