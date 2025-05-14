VSLAM was utilized to aid with camera calibration, calculating the mean reprojection error with the detected points for 3D and 2D image coordinates for rotated checkerboard images

Object points in 3D with corresponding image points in 2D with a solvePnP function to estimate the pose were used with aruco detection. 

solvePnP function was used to estimate the pose and aid with aruco detection for a sample image and distortion coefficients

kittiDataset was used to start VSLAM trajectory estimation and create matched pairs for plotting the respective camera trajectory
