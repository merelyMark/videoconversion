import os
import sys
from PIL import Image

def resize(filePath, factor, saveFilename):
    im = Image.open(filePath)
    print(filePath)
    w, h  = im.size

    newIm = im.resize((int(w*factor), int(h*factor)))
    # i am saving a copy, you can overrider orginal, or save to other folder
    #print(saveFilename) 
    newIm.save(saveFilename)
def bulkResize(imageFolder, factor):
    imgExts = ["png", "bmp", "jpg"]
    for path, dirs, files in os.walk(imageFolder):
        for fileName in files:
            ext = fileName[-3:].lower()
            if ext not in imgExts:
                continue

            saveFilename = os.path.join(os.getcwd(), fileName)
            if (not os.path.isfile(saveFilename)):
                try:
                    filePath = os.path.join(path, fileName)
                    resize(filePath, factor, saveFilename)
                except (OSError, IOError) as err:
                    print("Error, could not convert " + filePath + " " + str(err))
            else:
                print(saveFilename + " already exists.")

if __name__ == "__main__":
    imageFolder=sys.argv[1] # first arg is path to image folder
    resizeFactor=float(sys.argv[2])/100.0# 2nd is resize in %
    bulkResize(imageFolder, resizeFactor)
