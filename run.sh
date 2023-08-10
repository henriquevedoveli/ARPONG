#!/bin/bash

image="$1"
cam_source_value="$2"
video_device=/dev/video"${cam_source_value}"

echo $video_device

sudo docker run -it --privileged --network="host" --device $video_device --env="DISPLAY=$DISPLAY" -e "CAM_SOURCE=$cam_source_value" -v $(pwd)/src:/game $image
