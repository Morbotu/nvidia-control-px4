#!/usr/bin/env python3
import jetson.inference
import jetson.utils

import numpy as np


class DepthCamera:
    def __init__(self):
        self.__net = jetson.inference.depthNet()
        self.__depth_field = self.__net.GetDepthField()
        self.__depth_numpy = jetson.utils.cudaToNumpy(self.__depth_field)

    def get_depth_array(self, img):
        self.__net.Process(img)
        jetson.utils.cudaDeviceSynchronize()
        return self.__depth_numpy

if __name__ == "__main__":
    camera = jetson.utils.videoSource("csi://0")
    depth_camera = DepthCamera()
    while True:
        img = camera.Capture()
        pixel_closer = (depth_camera.get_depth_array(img) < 1.5).sum()
        if pixel_closer > 50000:
            print(f"To close {pixel_closer}")
