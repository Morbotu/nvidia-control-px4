#!/usr/bin/env python3
import scipy.misc
from math import floor, ceil
import jetson.utils
import paths
from ai_toolkit.detect_person import DetectionCamera
from ai_toolkit.messure_distance import DepthCamera
from control_px4.control_nvidia import MavLinkControl


camera = jetson.utils.videoSource("csi://0", argv=["--input-flip=rotate-180"])
depth_camera = DepthCamera()
detection_camera = DetectionCamera()
# controller = MavLinkControl()

while True:
    img = camera.Capture()
    detections, detect_img, shape_detections = detection_camera.get_detection_array(
        img)

    if len(detections) > 0:
        for detection in detections:
            depth_numpy, shape_depth = depth_camera.get_depth_array(img)
            proportions_row = shape_depth[0] / shape_detections[0]
            proportions_col = shape_depth[1] / shape_detections[1]
            detection_depth = depth_numpy[
                ceil(detection.Top * proportions_row):
                floor(detection.Bottom * proportions_row),
                ceil(detection.Left * proportions_col):
                floor(detection.Right * proportions_col),
                0
            ]

            if (detection_depth < 2.5).sum() > detection.Area * proportions_col * proportions_row * .40:
                print("Person to close")
            else:
                print("Person far enough")
    else:
        print("No one found")
