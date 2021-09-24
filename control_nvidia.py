#!/usr/bin/env python3

import rospy
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
import time


class MavLinkControl():
    def __init__(self):
        rospy.init_node("mav_control_node")
        self.rate = rospy.Rate(10)

        rospy.wait_for_service("/mavros/set_mode")
        self.mode_service = rospy.ServiceProxy("/mavros/set_mode", SetMode)
        rospy.wait_for_service("/mavros/cmd/arming")
        self.arm_service = rospy.ServiceProxy(
            '/mavros/cmd/arming', CommandBool)
        rospy.wait_for_service("/mavros/cmd/takeoff")
        self.takeoff_service = rospy.ServiceProxy(
            '/mavros/cmd/takeoff', CommandTOL)

    def arm(self):
        """
        Arm the throttle
        """
        return self.arm_service(True)

    def takeoff(self, height=30.0):
        """
        Arm the throttle, takeoff to a few feet, and set to guided mode
        """
        # Set to stabilize mode for arming
        #mode_resp = self.mode_service(custom_mode="0")
        mode_resp = self.mode_service(custom_mode="AUTO.TAKEOFF")
        self.arm()

        # Set to guided mode
        #mode_resp = self.mode_service(custom_mode="4")

        # Takeoff
        # takeoff_resp = self.takeoff_service(altitude=height, latitude=0, longitude=0, min_pitch=0, yaw=0)


        # return takeoff_resp
        return mode_resp

    def land(self):
        mode_resp = self.mode_service(custom_mode="AUTO.LAND")
        return mode_resp


if __name__ == "__main__":
    controller = MavLinkControl()
    controller.takeoff()
    time.sleep(20)
    controller.land()