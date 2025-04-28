#!/bin/bash

echo "The StellaVSLAM repository cloning is under progress..."
git clone --recurse-submodules https://github.com/stella-cv/stella_vslam.git
cd stella_vslam

echo "The StellaVSLAM Docker Image is building..."
docker build -t stella_vslam_desktop -f Dockerfile.Desktop .

echo "The Equirectangular Dataset (aist_living_lab_1) is being downloaded..."
mkdir -p ./dataset
cd dataset
wget https://github.com/stella-cv/stella_vslam/releases/download/20200401/aist_living_lab_1.zip
unzip aist_living_lab_1.zip
cd ..

echo "Starting StellaVSLAM Container with PangolinViewer..."

# Launching the Docker container
docker run -it --rm \
    --gpus all \
    --name stella_vslam_container \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd)/dataset:/home/user/dataset \
    stella_vslam_desktop \
    ./run_euroc_slam -v ./example/equirectangular/equirectangular.yaml -i ./dataset/aist_living_lab_1/video.mp4

echo "StellaVSLAM Launched Successfully!"
