import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pykitti

generatedBaseDirectory = '/content/'  
generatedSequenceNumber = '00' 

# Loading KITTI Odometry Dataset with generatedKittiDataset and pykitti.odometry
generatedKittiDataset = pykitti.odometry(generatedBaseDirectory, generatedSequenceNumber)

# The following ORB feature detector and matcher are available
generatedOrbDetector = cv2.ORB_create(3000)
generatedBFMatchingValue = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Load Calibration Data from previous task
generatedCalibrationData = np.load('generatedCameraCalibrationData.npz')
generatedCameraMatrix = generatedCalibrationData['GeneratedCameraMatrix']
generatedDistortionCoefficients = generatedCalibrationData['GeneratedDistortionCoefficients']

# Setting up the generatedPoseTrajectory for the camera
generatedPoseTrajectory = []
generatedCurrentPose = np.eye(4)

print("KITTI Dataset Loaded. Starting VSLAM Trajectory Estimation...")

for frameIndexValue in range(len(generatedKittiDataset) - 1):
    # Load consecutive frame images
    firstFrameImageValue = np.array(generatedKittiDataset.get_cam0(frameIndexValue))
    secondFrameImageValue = np.array(generatedKittiDataset.get_cam0(frameIndexValue + 1))

    firstGrayFrameValue = cv2.cvtColor(firstFrameImageValue, cv2.COLOR_RGB2GRAY)
    secondGrayFrameValue = cv2.cvtColor(secondFrameImageValue, cv2.COLOR_RGB2GRAY)

    # Detecting the ORB Features using key point and descriptor values
    firstKeyPointValue, firstDescriptorValue = generatedOrbDetector.detectAndCompute(firstGrayFrameValue, None)
    secondKeyPointValue, secondDescriptorValue = generatedOrbDetector.detectAndCompute(secondGrayFrameValue, None)

    if firstDescriptorValue is None or secondDescriptorValue is None:
        continue

    # Match Features
    generatedMatchPairs = generatedBFMatchingValue.match(firstDescriptorValue, secondDescriptorValue)
    generatedMatchPairs = sorted(generatedMatchPairs, key=lambda x: x.distance)

    if len(generatedMatchPairs) < 8:
        continue

    # Matched points extraction based on firstGeneratedPointSet and second point set with generatedMatchPairs
    firstGeneratedPointSet = np.float32([firstKeyPointValue[m.queryIdx].pt for m in generatedMatchPairs])
    secondGeneratedPointSet = np.float32([secondKeyPointValue[m.trainIdx].pt for m in generatedMatchPairs])

    # Estimation of essential matrix
    generatedEssentialMatrix, generatedMaskValue = cv2.findEssentialMat(
        firstGeneratedPointSet,
        secondGeneratedPointSet,
        generatedCameraMatrix,
        method=cv2.RANSAC,
        prob=0.999,
        threshold=1.0
    )

    # Relative camera poses, R and T
    _, generatedRotationalMatrix, generatedTranslationalVector, generatedMaskValue = cv2.recoverPose(
        generatedEssentialMatrix,
        firstGeneratedPointSet,
        secondGeneratedPointSet,
        generatedCameraMatrix
    )

    # Updating the camera trajectory
    generatedRelativeTransformation = np.eye(4)
    generatedRelativeTransformation[:3, :3] = generatedRotationalMatrix
    generatedRelativeTransformation[:3, 3] = generatedTranslationalVector.flatten()

    generatedCurrentPose = generatedCurrentPose @ np.linalg.inv(generatedRelativeTransformation)
    generatedPoseTrajectory.append(generatedCurrentPose[:3, 3])

generatedPoseTrajectory = np.array(generatedPoseTrajectory)

# Plotting the trajectory
plt.figure(figsize=(10,6))
plt.plot(generatedPoseTrajectory[:,0], generatedPoseTrajectory[:,2], label='Approximate Trajectory Value')
plt.xlabel('X position [meters]')
plt.ylabel('Z position [meters]')
plt.title('KITTI VSLAM Trajectory')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()

print("\nKITTI VSLAM Estimation Completed and Trajectory Plot Displayed!")
