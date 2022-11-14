#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Ozer Ozkahraman (ozero@kth.se)

import time, json, uuid, ssl, sys, os, rospy
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as mqtt_sub

from geographic_msgs.msg import GeoPoint
from std_msgs.msg import Float64, Bool, Empty

class Vehicle(object):
    def __init__(self):
        self.abort = None
        self.leak = None

        self.lat_lon = [None, None]
        self.utm_xy = [None, None]
        self.depth = None
        self.alt = None
        self.rpy = [None, None, None]

        self.battery_v = None
        self.motor_temp = None

        self.vbs = None
        self.lcg = None
        self.t1 = None
        self.t2 = None
        self.gps = None

        self.bt_last_wp = None



if __name__ == "__main__":
    rospy.init_node("smarc_mqtt_bridge_node")
