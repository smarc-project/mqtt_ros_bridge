#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Ozer Ozkahraman (ozero@kth.se)

import time, json, uuid, ssl, sys, os, rospy
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as mqtt_sub

from geographic_msgs.msg import GeoPoint
from std_msgs.msg import Float64

class WaraPSBridge(object):
    """
    A class to handle the specific things that
    wara-ps has, over mqtt
    """
    def __init__(self,
                 conn_params,
                 lat_lon_topic,
                 depth_topic,
                 robot_name="sam",
                 simulated=True,
                 tick_rate=0.3):
        # a list of messages from all the different parts of the handler
        self.feedback_messages = []

        self.robot_name = robot_name
        self.simulated = simulated
        self.tick_rate = tick_rate

        self._lat = -1
        self._lon = -1
        self._depth = -1
        self.lat_lon_sub = rospy.Subscriber(lat_lon_topic, GeoPoint, self._lat_lon_cb, queue_size=1)
        self.depth_sub = rospy.Subscriber(depth_topic, Float64, self._depth_cb, queue_size=1)


        # set up the mqtt client first
        self._uuid = uuid.uuid4().hex
        # one of: ground, air, surface, subsurface
        if 'sam' in self.robot_name or 'lolo' in self.robot_name:
            self._waraps_agent_type = "subsurface"
        else:
            self._waraps_agent_type = "surface"

        self._client = mqtt.Client(client_id = self.robot_name)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        use_waraps = True
        self.connected = False
        if use_waraps:
            try:
                # XXX this will probably break with ROS shenanigans...
                secrets_file = os.path.expanduser('~/.waraps_broker_SECRET')
                with open(secrets_file, 'r') as f:
                    user, pw = f.readlines()
                    user = user.strip('\n')
                    pw = pw.strip('\n')
            except Exception as e:
                print(e)
                print("You should have a file named '~/.waraps_broker_SECRET'")
                print("That file should look like:\n```\nusername\npassword\n```\n")
                print("Trying local one instead")
                use_waraps = False

            if use_waraps:
                self._client.username_pw_set(user, pw)
                self._client.tls_set(cert_reqs=ssl.CERT_NONE)
                self._client.tls_insecure_set(True)
                self._client.connect('broker.waraps.org', 8883, 60)
                print("Using waraps broker")
                self.connected = True

        if not use_waraps:
            try:
                self._client.connect(host = conn_params.get('host', 'localhost'),
                                     port = conn_params.get('port', 1884),
                                     keepalive = conn_params.get('keepalive', 60))
                print("Using local broker")
                self.connected = True
            except Exception as e:
                print(e)
                print("Can not connect to local mqtt broker!")

        self._client.loop_start()


    def _lat_lon_cb(self, msg):
        self._lat = msg.latitude
        self._lon = msg.longitude

    def _depth_cb(self, msg):
        self._depth = msg.data


    def _on_connect(self, client, userdata, flags, rc):
        """
        called when the client connection is successful
        fill in the topics list below to subscribe to all of them
        """
        self.feedback_messages.append("Connected with result code:{}".format(rc))

        # list of all the topics and their callbacks from waraps mqtt stuff
        # ((topic, qos), callback_fn)
        topics = [
            # XXX this is where all the data from wara-ps stuff will flow into ROS
        ]

        if len(topics) == 0:
            return

        for (t, qos),cb in topics:
            self._client.message_callback_add(t, cb)

        # subscribe to all the topics at once
        # this magic gets just the first tupiles of the topics list
        # as a list itself to be fed to subscribe
        tqos = list(list(zip(*topics))[0])
        self._client.subscribe(tqos)

    def _on_message(self, client, userdata, msg):
        """
        called when the client receives a message that no
        specific topic callback handles
        """
        self.feedback_messages.append("Got unhandled message:{} = {}".format(msg.topic, msg.payload))


    def _send_waraps(self, json_dict, topic):
        """
        A simple way to send general stuff related to waraps
        """
        msgstr = json.dumps(json_dict, sort_keys=True, indent=4, separators=(',',': '))
        # first one is one of: ground, air, surface, subsurface
        # second one is one of: real, simulation
        if self.simulated:
            prefix = "waraps/unit/{}/{}".format(self._waraps_agent_type, "simulation")
        else:
            prefix = "waraps/unit/{}/{}".format(self._waraps_agent_type, "real")

        self._client.publish("{}/{}/{}".format(prefix, self.robot_name, topic),
                             msgstr,
                             qos = 0,
                             retain = False)

    def _send_waraps_sensor(self):
        j = {}
        # probably negatives for depth?
        j["altitude"] = -self._depth
        j["latitude"] = self._lat
        j["longitude"] = self._lon
        j["rostype"] = "GeoPoint"
        self._send_waraps(j, 'sensor/position')

    def _send_waraps_sensorinfo(self):
        j = {}
        j['name'] = self.robot_name
        j['rate'] = self.tick_rate
        j['stamp'] = time.time()
        j['sensor_data_provided'] = ["position"]
        j['rostype'] = "SensorInfo"
        self._send_waraps(j, 'sensor_info')

    def _send_waraps_hearbeat(self):
        j = {}
        j['name'] = self.robot_name
        j['rate'] = self.tick_rate
        j['stamp'] = time.time()
        # XXX just a passive sensor until we know how to handle
        # wara-ps related commands and stuff
        j['levels'] = ["sensor"]
        j['agent-uuid'] = self._uuid
        j['agent-type'] = self._waraps_agent_type
        j['agent-description'] = "A SMaRC test robot"
        j['rostype'] = "HeartBeat"
        self._send_waraps(j, 'heartbeat')

    def tick(self):
        if self.connected:
            self.feedback_messages = []
            self._send_waraps_sensor()
            self._send_waraps_sensorinfo()
            self._send_waraps_hearbeat()
        else:
            self.feedback_messages = ["No connection"]

    def run(self):
        rate = rospy.Rate(self.tick_rate)
        while not rospy.is_shutdown():
            self.tick()
            rate.sleep()




if __name__ == "__main__":
    rospy.init_node("waraps_bridge_node")

    robot_name = rospy.get_param("~robot_name", "sam")

    # the mqtt-related stuff is shared with the ros-mqtt bridge
    params = rospy.get_param("~", {})
    try:
        mqtt_params = params.pop("mqtt")
        conn_params = mqtt_params.pop("connection")
        bridge_params = params.get("bridge", [])
        waraps_tickrate = params.get("waraps_tickrate", 3)
    except Exception as e:
        print(e)
        print("You need to run this program with roslaunch and pass the launch/config.yaml file as rosparam")
        sys.exit(1)

    # loop through all the topics in the config and find
    # the latlon and depth ones
    # so we can avoid having to specify them anywhere else
    for bridge_args in bridge_params:
        topic_from = bridge_args['topic_from']
        if "lat_lon" in topic_from:
            lat_lon_topic = topic_from
        if "depth" in topic_from:
            depth_topic = topic_from

    # check the list of topics to see if we have any that is under sim
    # to determine whether or not this is a simulated system
    s = os.popen("rostopic list | grep simulator")
    s = s.read()
    simulated = "simulator" in s


    wpsb = WaraPSBridge(conn_params,
                        lat_lon_topic,
                        depth_topic,
                        robot_name,
                        simulated=simulated,
                        tick_rate=waraps_tickrate)

    wpsb.run()









