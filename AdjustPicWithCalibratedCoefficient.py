import numpy as np
import cv2
import glob
import cv2.cv as cv
from tkFileDialog import askdirectory
from Tkinter import Tk
import time
from GetCameraCalibrationCoefficient import getCoefficient


def printUnitTimer(name, start, count):
    current = time.time()
    print name, ': ', (current - start) / count, ' s'


def printTimer(name, start):
    current = time.time()
    print name, ': ', current - start, ' s'


def convertPic(mtx, dist, inputPath, outputPath):
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (640, 640), 1, (640, 640))
    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(
        mtx, dist, None, newcameramtx, (640, 640), 5)
    x, y, w, h = roi

    test_images = glob.glob(inputPath + '/*.jpg')

    start = time.time()
    initial = start
    count = 0

    for filename in test_images:
        img = cv2.imread(filename)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        dst = dst[y:y + h, x:x + w]     # Crop the picture
        printTimer(str(count), start)
        start = time.time()
        count += 1
        cv2.imwrite(outputPath + '/' + str(count) + '.jpg', dst)

    printUnitTimer("Per Time Used ", initial, len(test_images))


def getPath():
    root = Tk()
    root.withdraw()
    InputPath = askdirectory(title="Choose Converting Picture Input Path")
    OutputPath = askdirectory(title="Choose Converting Picture Output Path")
    root.destroy()
    return InputPath, OutputPath

if __name__ == "__main__":
    """
    1. Choose trainning picture folder to generate camera calibration intrinsic and distortion coefficient
    2. Choose input path of converting picture folder
    3. Choose output path of convertin picture folder
    """
    mtx, dist = getCoefficient()
    inputPath, outputPath = getPath()
    convertPic(mtx, dist, inputPath, outputPath)


