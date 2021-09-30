#!/usr/bin/env python3
import scipy.misc
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
detections, detect_img, shape_detections = detection_camera.get_detection_array(img)
jetson.utils.saveImageRGBA("detection.jpg", detect_img, detect_img.width, detect_img.height)
depth_numpy, shape_depth = depth_camera.get_depth_array(img)
img = scipy.misc.toimage(depth_numpy[:, :, 0], mode="L")
img.save("depth.jpg")

proportions_shape_row = shape_depth[0]/shape_detections[0]
proportions_shape_col = shape_depth[1]/shape_detections[1]
if len(detections) > 0:
    detection_depth = depth_numpy[
        int(detections[0].Top * proportions_shape_row):
        int(detections[0].Bottum * proportions_shape_row),
        int(detections[0].Left*proportions_shape_col):
        int(detections[0].Right*()),
        0
    ]

    img = scipy.misc.toimage(detection_depth, mode="L")
    img.save("person_depth.jpg")
else:
    print("No one found")
