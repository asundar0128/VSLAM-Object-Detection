import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Loading the saved calibration data from earlier

generatedCalibrationData  = np.load('generatedCameraCalibrationData.npz')
generatedCameraMatrix = generatedCalibrationData['generatedCameraMatrix']
generatedDistortionCoefficients = generatedCalibrationData['generatedDistortionCoefficients']

# Object points in 3D with corresponding image points in 2D

objectPointsSimulation = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, -1],
    [1, 0, -1],
    [1, 1, -1],
    [0, 1, -1]
], dtype=np.float32)

imagePointsSimulation = np.array([
    [150, 150],
    [400, 150],
    [400, 400],
    [150, 400],
    [170, 170],
    [380, 170],
    [380, 380],
    [170, 380]
], dtype=np.float32)

# Using the solvePnP function to estimate the pose
generatedPoseEstimationSuccessFlag, generatedRotationalVectorValue, generatedTranslationalVectorValue = cv2.solvePnP(
    objectPointsSimulation,
    imagePointsSimulation,
    generatedCameraMatrix,
    generatedDistortionCoefficients
)

# Converting the rotational vector to a rotational matrix
generatedRotationalMatrix, _ = cv2.Rodrigues(generatedRotationalVectorValue)

print("\nPose Estimation Completed")
print("\The following rotation matrix:\n", generatedRotationalMatrix)
print("\The following translational vector:\n", generatedTranslationalVectorValue)

# Dictionary and parameters for aruco detection
generatedArucoDictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
generatedArucoParameters = cv2.aruco.DetectorParameters()
generatedArucoDetector = cv2.aruco.ArucoDetector(generatedArucoDictionary, generatedArucoParameters)

# Reading a sample image from the checkerboard
imagePathValue = './checkerboard-images/sample_marker.jpg'  # Place an image here manually
if os.path.exists(imagePathValue):
    generatedImageValue = cv2.imread(imagePathValue)
    generatedGrayImage = cv2.cvtColor(generatedImageValue, cv2.COLOR_BGR2GRAY)

    cornersFound, detectionIDS, _ = generatedArucoDetector.detectMarkers(generatedGrayImage)

    if len(cornersFound) > 0:
        rValue, rVectors, tVecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            cornersFound,
            0.05,
            generatedCameraMatrix,
            generatedDistortionCoefficients
        )
        for i in range(len(detectionIDS)):
            cv2.drawFrameAxes(GeneratedSampleImage, GeneratedCameraMatrix, GeneratedDistortionCoefficients, Rvecs[i], Tvecs[i], 0.1)

        plt.figure(figsize=(8,6))
        plt.imshow(cv2.cvtColor(generatedImageValue, cv2.COLOR_BGR2RGB))
        plt.title("Aruco Marker Pose Estimation Value")
        plt.axis('off')
        plt.show()
    else:
        print("\nAruco markers were not detected.")
else:
    print("\nAruco detection sample image not found.")
