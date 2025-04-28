import cv2
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

# The path where the checkerboard images are stored
generatedFolderPath = './checkerboard-images/'

# The checkerboard dimensions that are expected
generatedCheckerboardRows = 6
generatedCheckerboardColumns = 9
generatedSizeSquare = 1.0 

# Define 3D real-world object points for the checkerboard
generatedObjectPointsPattern = np.zeros((generatedCheckerboardRows * generatedCheckerboardColumns, 3), np.float32)
generatedObjectPointsPattern[:, :2] = np.mgrid[0:generatedCheckerboardColumns, 0:generatedCheckerboardRows].T.reshape(-1, 2) * generatedSizeSquare

# 3D points and 2D image coordinates accumulated via 2 lists
generatedObjectPoints = []
generatedImagePoints = []

# Checkerboard images are loaded
generatedFiles = glob.glob(os.path.join(generatedFolderPath, '*.jpg')) + glob.glob(os.path.join(generatedFolderPath, '*.png'))

# Valid image sizes processed here
generatedShapeImage = None

for generatedImageFile in generatedImageFiles:
    generatedImageValue = cv2.imread(generatedImageFile)
    generatedImageGrayValue = cv2.cvtColor(generatedImageValue, cv2.COLOR_BGR2GRAY)

    foundCornersFlagging, foundCorners = cv2.findChessboardCorners(generatedImageGrayValue, (generatedCheckerboardColumns, generatedCheckerboardRows), None)

    if foundCornersFlagging:
        if generatedShapeImage is None:
            generatedShapeImage = generatedImageGrayValue.shape[::-1]

        generatedCalibrationCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        modifiedCorners = cv2.cornerSubPix(generatedImageGrayValue, foundCorners, (11, 11), (-1, -1), GeneratedCalibrationCriteria)

        generatedObjectPoints.append(generatedObjectPointsPattern)
        generatedImagePoints.append(modifiedCorners)

        showImageValue = cv2.drawChessboardCorners(generatedImageValue, (generatedCheckerboardColumns, generatedCheckerboardRows), modifiedCorners, foundCornersFlagging)
        plt.figure(figsize=(8,6))
        plt.imshow(cv2.cvtColor(showImageValue, cv2.COLOR_BGR2RGB))
        plt.title(f"The following corners were detected: {os.path.basename(generatedImageFile)}")
        plt.axis('off')
        plt.show()

# Perform the camera calibration using the detected points
GeneratedCalibrationSuccessFlag, generatedCameraMatrix, generatedDistortionCoefficients, generatedRotationalVectors, generatedTranslationalVectors = cv2.calibrateCamera(
    generatedObjectPoints,
    generatedImagePoints,
    generatedShapeImage,
    None,
    None
)

print("\nThe camera calibration is over!")
print("\nThe following camera intrinsic matrix is generated:\n", generatedCameraMatrix)
print("\nThe following distortion coefficients were generated:\n", generatedDistortionCoefficients.flatten())

# Calculate the mean reprojection error
GeneratedTotalReprojectionError = 0
for i in range(len(GeneratedObjectPointsList)):
    generatedImagePointsProjected, _ = cv2.projectPoints(
        generatedObjectPoints[i],
        generatedRotationalVectors[i],
        generatedTranslationalVectors[i],
        generatedCameraMatrix,
        generatedDistortionCoefficients
    )
    generatedErrorValue = cv2.norm(generatedImagePoints[i], generatedImagePointsProjected, cv2.NORM_L2) / len(generatedImagePointsProjected)
    reprojectionErrorTotal += generatedErrorValue

meanProjectionError = reprojectionErrorTotal / len(generatedObjectPoints)
print("\nThe following mean reprojection error has been generated:", meanProjectionError)

# Save the calibration results into a compressed npz file
np.savez('generatedCameraCalibrationData.npz', 
         generatedCameraMatrix =generatedCameraMatrix, 
         generatedDistortionCoefficients = generatedDistortionCoefficients)

print("\nThe following calibration data has been saved to 'generatedCameraCalibrationData.npz'")
