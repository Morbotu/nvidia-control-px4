#!/usr/bin/env python3
import jetson.utils


class AiToolkit:
    def __init__(self, camera):
        self.net = None
        if camera:
            self.camera = jetson.utils.videoSource(camera)
