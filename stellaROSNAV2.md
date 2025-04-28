
Integrate **StellaVSLAM** into **ROS2 Navigation Stack (Nav2)** to enable a robot to localize and navigate **without a prior map** using Visual-Inertial Odometry and SLAM-based localization.


## 1. Pre-requisites

- Docker Installed
- Ubuntu 20.04 (recommended)
- ROS2 Foxy installed
- Nav2 Stack installed:  
  ```bash
  sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup

Commands:

mkdir -p ~/stella_ws/src
cd ~/stella_ws/src

# Clone StellaVSLAM and the ROS2 bridge
git clone --recurse-submodules https://github.com/stella-cv/stella_vslam.git
git clone https://github.com/stella-cv/stella_vslam_ros.git

# Install ROS2 Dependencies

cd ~/stella_ws
rosdep install --from-paths src --ignore-src -r -y

# Build workspace
colcon build --symlink-install
source install/setup.bash
