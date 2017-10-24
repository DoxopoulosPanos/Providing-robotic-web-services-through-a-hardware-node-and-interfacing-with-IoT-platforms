#Create String from Image, using Image_.py
import sys
from Image_ import Image

if __name__ == "__main__":
    path = sys.argv[1]
    img = Image(path)
    file = open('testfile.txt','w')
    imgBase64 = img.stringify_base64()
    file.write(imgBase64)
    file.close()

#example
#python Image2String.py "/home/panos/Desktop/Thesis/test/barcode/barcode10.png"
