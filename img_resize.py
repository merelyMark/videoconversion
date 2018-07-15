import os
import sys
from PIL import Image

def resize(folder, fileName, factor):
    filePath = os.path.join(folder, fileName)
    try:
        im = Image.open(filePath)
        print(filePath)
        w, h  = im.size
        saveFilename = os.path.join(os.getcwd(), fileName)

        if (not os.path.isfile(saveFilename)):
            newIm = im.resize((int(w*factor), int(h*factor)))
            # i am saving a copy, you can overrider orginal, or save to other folder
            #print(saveFilename) 
            newIm.save(saveFilename)
        else:
            print(saveFilename + " already exists.")
    except OSError as err:
        print("Error, could not convert " + filePath + " " + str(err))
def bulkResize(imageFolder, factor):
    imgExts = ["png", "bmp", "jpg"]
    for path, dirs, files in os.walk(imageFolder):
        for fileName in files:
            ext = fileName[-3:].lower()
            if ext not in imgExts:
                continue

            resize(path, fileName, factor)

if __name__ == "__main__":
    imageFolder=sys.argv[1] # first arg is path to image folder
    resizeFactor=float(sys.argv[2])/100.0# 2nd is resize in %
    bulkResize(imageFolder, resizeFactor)
