#!/usr/bin/env python3

import rospy
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL
from mavros_msgs.srv import ParamSet
from mavros_msgs.msg import ParamValue
import time


class MavLinkControl:
    def __init__(self):
        rospy.init_node("mav_control_node")
        self.rate = rospy.Rate(10)

        rospy.wait_for_service("/mavros/set_mode", timeout=30)
        self.mode_service = rospy.ServiceProxy("/mavros/set_mode", SetMode)
        rospy.loginfo("/mavros/set_mode service ready")
        rospy.wait_for_service("/mavros/cmd/arming", timeout=30)
        self.arm_service = rospy.ServiceProxy(
            '/mavros/cmd/arming', CommandBool)
        rospy.loginfo("/mavros/cmd/arming service ready")
        rospy.wait_for_service("/mavros/cmd/takeoff", timeout=30)
        self.takeoff_service = rospy.ServiceProxy(
            '/mavros/cmd/takeoff', CommandTOL)
        rospy.loginfo("/mavros/cmd/takeoff service ready")
        rospy.wait_for_service("/mavros/param/set", timeout=30)
        self.set_param_service = rospy.ServiceProxy("/mavros/param/set", ParamSet)
        rospy.loginfo("/mavros/param/set service ready")


    def arm(self):
        """
        Arm the throttle
        """
        arm_resp = self.arm_service(True)
        rospy.loginfo(arm_resp)
    
    def set_takeoff_height(self, height):
        set_resp = self.set_param_service("MIS_TAKEOFF_ALT", ParamValue(0, height))
        rospy.loginfo(set_resp)

    def takeoff(self, height=2.5):
        """
        Arm the throttle, takeoff to a few feet, and set to guided mode
        """

        self.set_takeoff_height(height)

        mode_resp = self.mode_service(custom_mode="AUTO.TAKEOFF")
        rospy.loginfo(mode_resp)
        self.arm()

    def land(self):
        mode_resp = self.mode_service(custom_mode="AUTO.LAND")
        rospy.loginfo(mode_resp)
    
    def hold(self):
        mode_resp = self.mode_service(custom_mode="AUTO.LOITER")
        rospy.loginfo(mode_resp)


if __name__ == "__main__":
    controller = MavLinkControl()
    controller.takeoff(5.0)
    time.sleep(20)
    controller.land()