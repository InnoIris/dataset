from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import numpy as np
import shutil

instruments = ['hammer']
## Custom dataset perfrom test-train split
dataset_folder = os.path.join('custom_dataset')
with open('custom_dataset.csv', 'w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for instrument in instruments:
    directory_name = os.path.join(dataset_folder, instrument)
    for filename in filter( lambda x: x.endswith('.jpg'), os.listdir(directory_name)):
      label = instrument
      filename_xml = filename[:-4] + '.xml'
      handler = None
      try:
        handler = open(os.path.join(directory_name, filename_xml)).read()
      except:
        print("Could not find", filename_xml)
        continue
      filename_str = os.path.join(directory_name, filename)
      soup = BeautifulSoup(handler, "xml")
      objs = soup.findAll('object')
      for obj in objs:
        xmin = int(obj.xmin.string)
        xmax = int(obj.xmax.string)
        ymin = int(obj.ymin.string)
        ymax = int(obj.ymax.string)
        row = [filename_str, xmin, xmax, ymin, ymax, instruments.index(instrument) + 1]
        writer.writerow(row)

df = pd.read_csv('custom_dataset.csv', header=None, names=['path', 'xmin', 'xmax', 'ymin', 'ymax', 'class'])
df.sample(frac=1)
msk = np.random.rand(len(df)) < 0.8
train = df[msk]
val = df[~msk]

# Copy the images into these folders
for index, row in train.iterrows():
  try:
    className = row['path'].split('/')[-2]
    image_file_name = row['path'].split('/')[-1]
    xml_file_name = image_file_name.replace(".jpg", ".xml")
    # Copy the image
    shutil.copy2(row['path'], os.path.join('train', className, f"custom_{image_file_name}"))
    # Copy the corresponding XML file
    shutil.copy2(row['path'].replace(".jpg", ".xml") , os.path.join('train', className, f"custom_{xml_file_name}"))
    print("Copy", row['path'], "to", 'train')
    train.at[index, 'path'] = os.path.join('train', className , image_file_name)
  except OSError as e:
    print(e)

print(train)

for index, row in val.iterrows():
  try:
    className = row['path'].split('/')[-2]
    image_file_name = row['path'].split('/')[-1]
    xml_file_name = image_file_name.replace(".jpg", ".xml")
    # Copy the image
    shutil.copy2(row['path'], os.path.join('validation', className, f"custom_{image_file_name}"))
    # Copy the corresponding XML file
    shutil.copy2(row['path'].replace(".jpg", ".xml") , os.path.join('validation', className, f"custom_{xml_file_name}"))
    print("Copy", row['path'], "to", 'validation')
    val.at[index, 'path'] = os.path.join('validation', className , image_file_name)
  except OSError as e:
    print(e)

print(val)

os.remove('custom_dataset.csv')