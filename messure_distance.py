#!/usr/bin/env python3
import jetson.inference
import jetson.utils

import numpy as np


class DepthCamera:
    def __init__(self):
        self.net = jetson.inference.depthNet()
        self.depth_field = self.net.GetDepthField()
        self.depth_numpy = jetson.utils.cudaToNumpy(self.depth_field)
        self.camera = jetson.utils.videoSource("csi://0")

    def distance_reached(self, threshold_distance=2.0):
        img = self.camera.Capture()
        self.net.Process(img)
        jetson.utils.cudaDeviceSynchronize()
        
        return (self.depth_numpy < threshold_distance).sum()

if __name__ == "__main__":
    depth_camera = DepthCamera()
    while True:
        pixel_closer = depth_camera.distance_reached(1.5)
        if pixel_closer > 50000:
            print(f"To close {pixel_closer}")