# mqtt_ros_bridge
Two nodes to publish ROS stuff into MQTT, for use with node-red GUIs.
`roslaunch mqtt_ros_bridge mqtt_ros_bridge.launch robot_name:=XXX broker_addr:=XXX broker_port:=XXX`

By default, connects to the smarc server with robot_name sam.


Can connect to the wara-ps GUI if you have a file `~/.waraps_broker_SECRET` that looks like:
```
username
password
```

# Noetic installation
```
apt install ros-noetic-mqtt-bridge
apt install python-paho-mqtt
pip install inject
```

# Melodic installation
```
apt install ros-melodic-mqtt-bridge
apt install python-paho-mqtt
pip2 install --user Inject==3.5.4
```
