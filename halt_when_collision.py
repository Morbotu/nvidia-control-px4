from control_nvidia import MavLinkControl
from messure_distance import DepthCamera


depth_camera = DepthCamera()
controller = MavLinkControl()

while True:
    pixel_closer = depth_camera.distance_reached(1.5)
    if pixel_closer > 50000:
        controller.hold()
