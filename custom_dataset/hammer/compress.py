import os
import sys
import cv2
from PIL import Image
import xml.etree.ElementTree as ET
from xml.dom import minidom

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the       
        # # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized,r

def annotations(file, ratio):
    filename_xml = file[:-4] + '.xml'
    try:
        tree = ET.parse(os.path.join(os.getcwd(), filename_xml))
        root = tree.getroot()
        #considers oen and only one obj exists in the image 
        x2 = root.find('object').find('bndbox').find('xmin').text 
        y2 = root.find('object').find('bndbox').find('ymin').text 
        x1 = root.find('object').find('bndbox').find('xmax').text 
        y1 = root.find('object').find('bndbox').find('ymax').text
        x2 = float(x2) * ratio
        x1 = float(x1) * ratio
        y1 = float(y1) * ratio
        y2 = float(y2) * ratio
        root.find('object').find('bndbox').find('xmin').text = str(int(x2))
        root.find('object').find('bndbox').find('ymin').text = str(int(y2))
        root.find('object').find('bndbox').find('xmax').text = str(int(x1))
        root.find('object').find('bndbox').find('ymax').text = str(int(y1))

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(os.path.join(os.getcwd(), filename_xml), "w") as f:
            f.write(xmlstr)
        return (int(x2), int(y2), int(x1), int(y1))
    except xml.etree.ElementTree.ParseError as e:
        print (file, str(e))
        return


def compressMe(file, verbose=False):
    filepath = os.path.join(os.getcwd(), file)
    img = cv2.imread(filepath)
    image, ratio = image_resize(img, width = 440)
    x1,y1,x2,y2 = annotations(file,ratio)
    cv2.imwrite(filepath, image)
    # visualize(image, x1,y1,x2,y2)
    # print(image.shape)


def visualize(image, x1, y1,x2,y2):
    demo = cv2.rectangle(image, (x1,y1), (x2,y2), (255, 0, 0) , 2)
    cv2.imshow("test", demo)
    key = cv2.waitKey(500)#pauses for 0.5 seconds before fetching next image
    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()  
	

def main():
    pwd = os.getcwd()
    tot = 0
    num = 0
    for file in os.listdir(pwd):
        if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
            num += 1
            compressMe(file)
    print(num)
    print ("Done")
	

if __name__ == "__main__":
	main()