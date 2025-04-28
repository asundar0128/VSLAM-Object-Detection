# ======================
# task2_pose_estimation.py (Generated Variable Style)
# ======================

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Load previously saved calibration data
CalibrationData = np.load('generatedCameraCalibrationData.npz')
GeneratedCameraMatrix = CalibrationData['GeneratedCameraMatrix']
GeneratedDistortionCoefficients = CalibrationData['GeneratedDistortionCoefficients']

# Simulated object points (3D) and corresponding image points (2D)
ObjectPointsSim = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, -1],
    [1, 0, -1],
    [1, 1, -1],
    [0, 1, -1]
], dtype=np.float32)

ImagePointsSim = np.array([
    [150, 150],
    [400, 150],
    [400, 400],
    [150, 400],
    [170, 170],
    [380, 170],
    [380, 380],
    [170, 380]
], dtype=np.float32)

# SolvePnP to estimate pose
PoseEstimationSuccessFlag, GeneratedRotationVector, GeneratedTranslationVector = cv2.solvePnP(
    ObjectPointsSim,
    ImagePointsSim,
    GeneratedCameraMatrix,
    GeneratedDistortionCoefficients
)

# Convert rotation vector to rotation matrix
GeneratedRotationMatrix, _ = cv2.Rodrigues(GeneratedRotationVector)

print("\n✅ Pose Estimation Completed")
print("\nGenerated Rotation Matrix:\n", GeneratedRotationMatrix)
print("\nGenerated Translation Vector:\n", GeneratedTranslationVector)

# =======================
# ArUco Marker Detection Example
# =======================

# Create dictionary and parameters for ArUco detection
GeneratedArucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
GeneratedArucoParams = cv2.aruco.DetectorParameters()
GeneratedArucoDetector = cv2.aruco.ArucoDetector(GeneratedArucoDict, GeneratedArucoParams)

# Read a sample image
SampleImagePath = './checkerboard-images/sample_marker.jpg'  # Place an image here manually
if os.path.exists(SampleImagePath):
    GeneratedSampleImage = cv2.imread(SampleImagePath)
    GeneratedGraySampleImage = cv2.cvtColor(GeneratedSampleImage, cv2.COLOR_BGR2GRAY)

    CornersDetected, IDsDetected, _ = GeneratedArucoDetector.detectMarkers(GeneratedGraySampleImage)

    if len(CornersDetected) > 0:
        RetVal, Rvecs, Tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            CornersDetected,
            0.05,  # Marker length (adjust as needed)
            GeneratedCameraMatrix,
            GeneratedDistortionCoefficients
        )
        for i in range(len(IDsDetected)):
            cv2.drawFrameAxes(GeneratedSampleImage, GeneratedCameraMatrix, GeneratedDistortionCoefficients, Rvecs[i], Tvecs[i], 0.1)

        plt.figure(figsize=(8,6))
        plt.imshow(cv2.cvtColor(GeneratedSampleImage, cv2.COLOR_BGR2RGB))
        plt.title("Generated ArUco Marker Pose Estimation")
        plt.axis('off')
        plt.show()
    else:
        print("\n⚠️ No ArUco markers detected.")
else:
    print("\n⚠️ Sample image for ArUco detection not found.")
