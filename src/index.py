from ai_toolkit.detect_person import DetectionCamera
from ai_toolkit.messure_distance import DepthCamera
from control_px4.control_nvidia import MavLinkControl

depth_camera = DepthCamera(camera="csi://0")
detection_camera = DetectionCamera(camera="csi://0")
controller = MavLinkControl()

while True:
    detections, shape_detections = detection_camera.get_detection_array()
    depth_numpy, shape_depth = depth_camera.get_depth_array()
