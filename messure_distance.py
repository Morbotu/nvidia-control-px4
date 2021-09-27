#!/usr/bin/env python3
import jetson.inference
import jetson.utils

import numpy as np


class DepthCamera:
    def __init__(self):
        # load mono depth network
        self.net = jetson.inference.depthNet()

        # depthNet re-uses the same memory for the depth field,
        # so you only need to do this once (not every frame)
        self.depth_field = self.net.GetDepthField()

        # cudaToNumpy() will map the depth field cudaImage to numpy
        # this mapping is persistent, so you only need to do it once
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
        distance = depth_camera.distance_reached(1.5)
        if distance > 50000:
            print(f"To close {distance}")