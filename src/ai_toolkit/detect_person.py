#!/usr/bin/env python3
import jetson.inference
import jetson.utils
import numpy as np
from ai_kit import AiToolkit


class DetectionCamera(AiToolkit):
    def __init__(self, net="pednet", threshold=0.6, camera=None):
        super().__init__(jetson.inference.detectNet(net, threshold=threshold), camera=camera)

    def get_detection_array(self, img=None):
        img = self.get_img(img)
        detections = self.net.Detect(img)
        return detections, img, np.shape(img)


if __name__ == "__main__":
    camera = jetson.utils.videoSource("csi://0")
    detection_camera = DetectionCamera()
    while True:
        img = camera.Capture()
        detections, img, shape = detection_camera.get_detection_array(img)
        print([person.Center for person in detections], shape)
