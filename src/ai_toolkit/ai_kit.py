#!/usr/bin/env python3
import jetson.utils


class AiToolkit:
    def __init__(self, net, camera=None):
        self.net = net
        if camera:
            self.camera = jetson.utils.videoSource(camera)

    def get_img(self, img):
        if not img:
            if self.camera:
                img = self.camera.Capture()
            else:
                raise Exception("No camera found")
        return img
