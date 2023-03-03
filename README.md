# mqtt_ros_bridge
A node to publish ROS stuff into MQTT, for use with node-red GUI of SMaRC.
`roslaunch mqtt_ros_bridge mqtt_ros_bridge.launch robot_name:=XXX broker_addr:=XXX broker_port:=XXX`

By default, connects to the smarc server with robot_name sam.

## mqtt_nodered
Contains the settings and docker files to setup the SMaRC node-red GUI.

# Installation
```
apt install ros-{$ROS_DISTRO}-mqtt-bridge
apt install python-paho-mqtt
```

If `{$ROS_DISTRO} == Noetic`: `pip install inject`

If `{$ROS_DISTRO} == Melodic`: `pip2 install --user Inject==3.5.4`
Because melodic is now ancient and needs special elderly care...
