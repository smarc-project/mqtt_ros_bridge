# mqtt_ros_bridge
A node to publish ROS stuff into MQTT, for use with node-red GUI of SMaRC.
`roslaunch mqtt_ros_bridge mqtt_ros_bridge.launch robot_name:=XXX broker_addr:=XXX broker_port:=XXX`

By default, connects to the smarc server with robot_name sam.

## mqtt_nodered
Contains the settings and docker files to setup the SMaRC node-red GUI.
