import numpy as np
import cv2
import glob
import cv2.cv as cv
from tkFileDialog import askdirectory
from Tkinter import Tk

CV_CALIB_USE_INTRINSIC_GUESS = 1
CV_CALIB_ZERO_TANGENT_DIST = 8
CV_CALIB_RATIONAL_MODEL = 16384


def getCoefficient():
    """
    Calculate Fisheye Camera Calibration Intrinsic and Distortion Coefficient Using OpenCV Camera Calibration and 3D Reconstruction library.
    Prerequisite: A set of CHESS BOARD pictures for trainning.
    Reference:
    1. http://docs.opencv.org/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#camera-calibration-and-3d-reconstruction
    2. http://docs.opencv.org/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
    3. http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration
    4. http://stackoverflow.com/questions/14841683/camera-calibration-opencv
    5. http://stackoverflow.com/questions/27348139/camera-calibration-with-opencv-findchessboardcorners-returns-false
    """
    # Get Training Pictures Directory Path
    root = Tk()
    root.withdraw()
    Train_Image_Path = askdirectory(title="Choose Training Picture Folder")
    root.destroy()

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:6, 0:9].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(Train_Image_Path + '/*.jpg')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)	# Find chess board corners

        if ret is True:		# Corners Found
            objpoints.append(objp)
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            # cv2.drawChessboardCorners(img, (6, 9), corners, ret)

    cv2.destroyAllWindows()

    # Camera Matrix initial coefficient guess (Have to change flags in cv2.calibrateCamera if without initial guess. See Reference 1)
    mtx_init = np.zeros((3, 3), np.float32)
    mtx_init[0][0] = 310.940583445
    mtx_init[0][2] = 320.0
    mtx_init[1][1] = 310.940583445
    mtx_init[1][2] = 320.0
    mtx_init[2][2] = 1.0

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], cameraMatrix = mtx_init, flags = CV_CALIB_USE_INTRINSIC_GUESS + CV_CALIB_ZERO_TANGENT_DIST + CV_CALIB_RATIONAL_MODEL)

    return mtx, dist


if __name__ == "__main__":
    mtx, dist = getCoefficient()
    print 'mtx = ', mtx
    print 'dist = ', dist
