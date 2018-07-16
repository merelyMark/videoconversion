import os, time
from stat import *

import sys
from PIL import Image,  ExifTags

TEST_DATETIME = False
def fix_orientation(exifdata):

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break
    if (exifdata != None):
        exif=dict(exifdata.items())

        if (orientation in exif):
            if exif[orientation] == 3:
                return 180
            elif exif[orientation] == 6:
                return 270
            elif exif[orientation] == 8:
                return 90
    return 0


def bulkFixOrientation(imageFolder):
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
                    im = Image.open(filePath)
                    if (hasattr(im, '_getexif')):    
                        degrees = fix_orientation(im._getexif())
                        im = im.rotate(degrees, expand=True)
                    im.save(saveFilename)
                    im.close()

                except (OSError, IOError) as err:
                    print("Error, could not convert " + filePath + " " + str(err))
            else:
                print(saveFilename + " already exists.")

def fix_datetime(filePath, outfile):
    in_st = os.stat(filePath)
    in_atime = in_st[ST_ATIME]
    in_mtime = in_st[ST_MTIME]

    out_st = os.stat(outfile)
    out_atime = out_st[ST_MTIME]
    print (time.ctime(out_atime) + ' ' + time.ctime(in_mtime))
    if (not TEST_DATETIME):
        os.utime(outfile, (out_atime, in_mtime))

def bulkFixdatetime(imageFolder):
    imgExts = ["png", "bmp", "jpg"]
    for path, dirs, files in os.walk(imageFolder):
        for fileName in files:
            ext = fileName[-3:].lower()
            if ext not in imgExts:
                continue

            saveFilename = os.path.join(os.getcwd(), fileName)
            try:
                filePath = os.path.join(path, fileName)
                fix_datetime(filePath, saveFilename)
            except (OSError, IOError) as err:
                print("Error, could not convert " + filePath + " " + str(err))

def resize(filePath, factor, saveFilename):
    im = Image.open(filePath)
    print(filePath)
    w, h  = im.size

    newIm = im.resize((int(w*factor), int(h*factor)))
    if (hasattr(im, '_getexif')):
        degrees = fix_orientation(im._getexif())
        print(degrees)
        newIm = newIm.rotate(degrees, expand=True)
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
                    fix_datetime(filePath, saveFilename)
                except (OSError, IOError) as err:
                    print("Error, could not convert " + filePath + " " + str(err))
            else:
                print(saveFilename + " already exists.")

if __name__ == "__main__":
    imageFolder=sys.argv[1] # first arg is path to image folder
    resizeFactor=float(sys.argv[2])/100.0# 2nd is resize in %
    bulkResize(imageFolder, resizeFactor)
    #bulkFixdatetime(imageFolder)
    #bulkFixOrientation(imageFolder)
