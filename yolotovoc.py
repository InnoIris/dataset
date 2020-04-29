import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2
import numpy

folder = 'train/'
instruments = ['hammer']

def conversion(line, width, height, img):
    x, y, w, h = float(line[1]), float(line[2]), float(line[3]), float(line[4])
    x1, y1 = int((x + w/2.0)*width), int((y + h/2.0)*height)
    x2, y2 = int((x - w/2.0)*width) , int((y - h/2.0)*height)
    return str(x1),str(y1),str(x2),str(y2)

module_dir = os.getcwd() + '/' + folder
classes = None
try:
    classes = open(os.path.join(module_dir, 'classes.txt')).read().splitlines()
    for instrument in instruments:
        dir_name = os.path.join(module_dir, instrument)
        for filename in os.listdir(dir_name):
            if(filename[-4:]=='.txt'):
                tree = ET.parse(os.path.join(module_dir, 'skeleton.xml'))
                root = tree.getroot()
                # with open(filename[:-4]+'.xml', mode=w) as file:
                txt = None
                try: 
                    txt = open(os.path.join(dir_name,filename)).read().splitlines()
                    img = cv2.imread(os.path.join(dir_name,filename[:-4]+'.jpg'))
                    if img.size == 0:
                        print("img size not loaded")
                        pass
                    height, width, channels = img.shape
                    root.find('folder').text = instrument
                    root.find('filename').text = filename[:-4]+'.jpg'
                    root.find('path').text = os.path.join(dir_name,filename[:-4]+'.jpg')
                    (root.find('size').find('width')).text = str(width)
                    (root.find('size').find('height')).text = str(height)
                    (root.find('size').find('depth')).text = str(channels)
                    for idx in range(len(txt)):
                        line = txt[idx].split(' ')
                        x1,y1,x2,y2 = conversion(line, width, height, img)
                        if idx==0:
                            root.find('object').find('name').text = classes[int(line[0])]
                            root.find('object').find('bndbox').find('xmin').text = x2
                            root.find('object').find('bndbox').find('ymin').text = y2
                            root.find('object').find('bndbox').find('xmax').text = x1
                            root.find('object').find('bndbox').find('ymax').text = y1
                        else:
                            root.append(root.makeelement('object',{}))
                            root[6+idx].append(root[6+idx].makeelement('name',{}))
                            root[6+idx][0].text = classes[int(line[0])]
                            root[6+idx].append(root[6+idx].makeelement('pose',{}))
                            root[6+idx][1].text = 'Unspecified'
                            root[6+idx].append(root[6+idx].makeelement('truncated',{}))
                            root[6+idx][2].text = '0'
                            root[6+idx].append(root[6+idx].makeelement('difficult',{}))
                            root[6+idx][3].text = '0'
                            root[6+idx].append(root[6+idx].makeelement('bndbox',{}))
                            root[6+idx][4].append(root[6+idx][4].makeelement('xmin',{}))
                            root[6+idx][4][0].text = x2
                            root[6+idx][4].append(root[6+idx][4].makeelement('ymin',{}))
                            root[6+idx][4][1].text = y2
                            root[6+idx][4].append(root[6+idx][4].makeelement('xmax',{}))
                            root[6+idx][4][2].text = x1
                            root[6+idx][4].append(root[6+idx][4].makeelement('ymax',{}))
                            root[6+idx][4][3].text = y1
                    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
                    with open(os.path.join(dir_name,filename[:-4]+'.xml'), "w") as f:
                        f.write(xmlstr)
                except OSError:
                    print('Could not open .txt file')
                    continue
except OSError:
    print("Could not find classes")


