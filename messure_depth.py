import jetson.inference
import jetson.utils

import numpy as np

# load mono depth network
net = jetson.inference.depthNet()

# depthNet re-uses the same memory for the depth field,
# so you only need to do this once (not every frame)
depth_field = net.GetDepthField()

# cudaToNumpy() will map the depth field cudaImage to numpy
# this mapping is persistent, so you only need to do it once
depth_numpy = jetson.utils.cudaToNumpy(depth_field)

print(f"depth field resolution is {depth_field.width}x{depth_field.height}, format={depth_field.format}")

camera = jetson.utils.videoSource("csi://0")

while True:
    img = camera.Capture()
    net.Process(img)
    jetson.utils.cudaDeviceSynchronize()
	
    min_depth = np.amin(depth_numpy)
    max_depth = np.amax(depth_numpy)
    print(max_depth)
