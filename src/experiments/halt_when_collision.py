#!/usr/bin/env python3
from src.control_px4.control_nvidia import MavLinkControl
from src.ai_toolkit.messure_distance import DepthCamera
import jetson.utils


depth_camera = DepthCamera()
controller = MavLinkControl()
camera = jetson.utils.videoSource("csi://0")

while True:
    img = camera.Capture()
    pixel_closer = (depth_camera.get_depth_array(img) < 1.5).sum()
    if pixel_closer > 50000:
        controller.hold()
