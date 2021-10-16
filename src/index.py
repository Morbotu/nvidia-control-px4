#!/usr/bin/env python3
import scipy.misc
from math import floor, ceil
import jetson.utils
import paths
from ai_toolkit.detect_person import DetectionCamera
from ai_toolkit.messure_distance import DepthCamera
from control_px4.control_nvidia import MavLinkControl


camera = jetson.utils.videoSource("csi://0", argv=["--input-flip=rotate-180"])
depth_camera = DepthCamera()
detection_camera = DetectionCamera()
# controller = MavLinkControl()

# while True:
img = camera.Capture()
jetson.utils.saveImageRGBA("original.jpg", img, img.width, img.height)
detections, detect_img, shape_detections = detection_camera.get_detection_array(
    img)
jetson.utils.saveImageRGBA("detection.jpg", detect_img,
                           detect_img.width, detect_img.height)

if len(detections) > 0:
    depth_numpy, shape_depth = depth_camera.get_depth_array(img)
    img = scipy.misc.toimage(depth_numpy[:, :, 0], mode="L")
    img.save("depth.jpg")

    proportions_row = shape_depth[0] / shape_detections[0]
    proportions_col = shape_depth[1] / shape_detections[1]
    for detection in detections:
        detection_depth = depth_numpy[
            ceil(detection.Top * proportions_row):
            floor(detection.Bottom * proportions_row),
            ceil(detection.Left * proportions_col):
            floor(detection.Right * proportions_col),
            0
        ]

        img = scipy.misc.toimage(detection_depth, mode="L")
        img.save("person_depth.jpg")

        if (detection_depth < 2.5).sum() > detection_depth.size * .99:
            print("Person to close")
        else:
            print("Person far enough")
else:
    print("No one found")
