## VSLAM and Object Detection

This repository explores Visual Simultaneous Localization and Mapping (VSLAM) techniques combined with object detection. The project covers camera calibration, pose estimation using ArUco markers, and trajectory estimation using the KITTI dataset.

## Key Features

- Camera Calibration: Utilized VSLAM principles to perform camera calibration by calculating the mean reprojection error. This involves mapping 3D object points to 2D image coordinates using rotated checkerboard images.
- Pose Estimation (solvePnP): Implemented solvePnP to estimate camera pose by matching 3D object points with 2D image points, specifically aiding in ArUco marker detection.
- Trajectory Estimation: Used the KITTI Dataset to initialize VSLAM trajectory estimation. The system creates matched feature pairs to plot the camera's movement trajectory over time.
- Distortion Correction: Integrated distortion coefficients to refine pose accuracy in sample images.

## Project Structure

- Calibration: Scripts for checkerboard detection and reprojection error calculation.
- Detection: ArUco marker tracking and pose estimation logic.
- Mapping: Trajectory plotting and KITTI dataset integration.

## Mathematical Overview

The core of the pose estimation relies on minimizing the back-projection error. For a set of 3D points $P_i$ and their corresponding 2D projections $u_i$, we estimate the rotation $R$ and translation $t$ such that:

$$\sum_{i} \| u_i - \text{project}(P_i; R, t, K) \|^2$$

where $K$ represents the intrinsic camera matrix.
