#!/usr/bin/env python3
import jetson.inference
import jetson.utils
from ai_kit import AiToolkit
import numpy as np


class DepthCamera(AiToolkit):
    def __init__(self, net="monodepth-mobilenet", camera=None):
        super().__init__(jetson.inference.depthNet(net), camera=camera)
        self.depth_field = self.net.GetDepthField()
        self.depth_numpy = jetson.utils.cudaToNumpy(self.depth_field)

    def get_depth_array(self, img=None):
        img = self.get_img(img)
        self.net.Process(img)
        jetson.utils.cudaDeviceSynchronize()
        return self.depth_numpy, np.shape(img)


if __name__ == "__main__":
    camera = jetson.utils.videoSource("csi://0")
    depth_camera = DepthCamera()
    while True:
        img = camera.Capture()
        pixel_closer = (depth_camera.get_depth_array(img)[0] < 1.5).sum()
        if pixel_closer > 50000:
            print(f"To close {pixel_closer}")
