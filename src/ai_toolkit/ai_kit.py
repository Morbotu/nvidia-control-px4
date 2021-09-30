#!/usr/bin/env python3
import jetson.utils


class AiToolkit:
    def __init__(self, net, camera=None):
        self.net = net
        if camera:
            self.camera = jetson.utils.videoSource(camera)
