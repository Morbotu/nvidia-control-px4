#!/usr/bin/env python3
import jetson.inference
import jetson.utils
import numpy as np


class DetectionCamera:
    def __init__(self):
        self._net = jetson.inference.detectNet("pednet", threshold=0.6)

    def get_detection_array(self, img):
        detections = self._net.Detect(img)
        return detections, np.shape(img)


if __name__ == "__main__":
    camera = jetson.utils.videoSource("csi://0")
    detection_camera = DetectionCamera()
    while True:
        img = camera.Capture()
        detections, shape = detection_camera.get_detection_array(img)
        print([person.Center for person in detections], shape)
