from ai_toolkit.detect_person import DetectionCamera
from ai_toolkit.messure_distance import DepthCamera
from control_px4.control_nvidia import MavLinkControl
import scipy.misc

depth_camera = DepthCamera(camera="csi://0")
detection_camera = DetectionCamera(camera="csi://0")
controller = MavLinkControl()

# while True:
detections, shape_detections = detection_camera.get_detection_array()
depth_numpy, shape_depth = depth_camera.get_depth_array()

proportions_shape_row = shape_depth[0]/shape_detections[0]
proportions_shape_col = shape_depth[1]/shape_detections[1]
detection_depth = depth_numpy[
    int(detections.Top * proportions_shape_row):
    int(detections.Bottum * proportions_shape_row),
    int(detections.Left*proportions_shape_col):
    int(detections.Right*()),
    0
]

img = scipy.misc.toimage(detection_depth, mode="L")