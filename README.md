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

## Local installation
1- Install docker and docker-compose with your preffered method.

2- Start up the docker containers:
```
git clone https://github.com/smarc-project/smarc_nodered
cd smarc_nodered/mqtt_nodered
docker-compose up
```
(Ignore the error loading credentials and flows, we will load them later)

3- Connect to node-red flow on your browser: http://127.0.0.1:1880/flow/

4- Ask me for the username and password.

5- Ignore the welcome-wagon, press the 'x' on the pop-up

6- On the second pop-up about projects, click "Clone Repository"

7- Enter your name and email. This is used for commits and such. Not your github username and password!

8- Github settings

8-1- Git repository url: https://github.com/KKalem/smarc_nodered_cnc

8-2- Fill your github username and password (or gpg key)

8-3- Credentials encryption key: usual smarc password but with a 2.  

8-4- Click Clone Project

9- You will see a pop-up telling you that some stuff is missing, close the pop-up

10- Hamburger-menu on top right > projects > project settings > dependencies

11- Click the install buttons on each one. You can spam them. Pop-ups will come, click install again.

12- In the background, you will see a MESS. Ignore the dread for now. Close the open pop-up.

13- Go back to the terminal where you ran `docker-compose up`, Ctrl-C, and again `docker-compose up`. This restarts everything.

14- Back to the browser. Refresh the page. The mess should be gone and no pop-ups should appear. You have now a working copy of the node-red interface.

### Using the local installation
#### Updating
To update the nodered flows, click the small git-branch icon on the right-panel, click commit history at the bottom, and then the up-down arrows right under.

Click pull.

Deploy the changes with the top-right red button.

#### The UI
Its here: http://127.0.0.1:1880/ui

Use the usual smarc username and pw.

#### Connect your robot to this GUI
The robot connects to the local AND cloud-based GUIs at the same time. You shouldn't need to do anything.
