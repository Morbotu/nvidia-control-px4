#!/usr/bin/env python3
from messure_distance import DepthCamera
from detect_person import DetectionCamera
import jetson.utils
import numpy as np


class AiToolkit(DepthCamera, DetectionCamera):
    pass

if __name__ == "__main__":
    camera = jetson.utils.videoSource("csi://0")
    ai_toolkit = AiToolkit()
    while True:
        img = camera.Capture()
        detections, shape = ai_toolkit.get_detection_array(img)
        print([person.Center for person in detections], shape)
