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
      objs = soup.findAll('object')
      for obj in objs:
        xmin = int(obj.xmin.string)
        xmax = int(obj.xmax.string)
        ymin = int(obj.ymin.string)
        ymax = int(obj.ymax.string)
        row = [filename_str, xmin, xmax, ymin, ymax, instruments.index(instrument) + 1]
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
      objs = soup.findAll('object')
      for obj in objs:
        xmin = int(obj.xmin.string)
        xmax = int(obj.xmax.string)
        ymin = int(obj.ymin.string)
        ymax = int(obj.ymax.string)
        row = [filename_str, xmin, xmax, ymin, ymax, instruments.index(instrument) + 1]
        writer.writerow(row)
