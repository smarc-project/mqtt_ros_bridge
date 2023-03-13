# smarc_nodered
A node to publish ROS stuff into MQTT, for use with node-red GUI of SMaRC.
`roslaunch smarc_nodered smarc_nodered.launch robot_name:=XXX broker_addr:=XXX broker_port:=XXX`

By default, connects to the smarc server with robot_name sam.

## mqtt_nodered
Contains the settings and docker files to setup the SMaRC node-red GUI.
Also contains mapserver settings for Sweden bathymetry dataset(private).

# Installation
```
apt install ros-{$ROS_DISTRO}-mqtt-bridge
apt install python-paho-mqtt
```

If `{$ROS_DISTRO} == Noetic`: `pip install inject`

If `{$ROS_DISTRO} == Melodic`: `pip2 install --user Inject==3.5.4`
Because melodic is now ancient and needs special elderly care...
