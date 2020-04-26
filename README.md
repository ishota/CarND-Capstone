This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Please use **one** of the two installation options, either native **or** docker installation.


Done by Shota Ishikawa.

## Acceleration Profiles

### Sigmoid Smooth Acceleration Profile

Waypoint velocity calculation algorithm proposed at walkthrough is simple to implement. But it has a drawback: the car starts to brake abruptly causing high jerk that is not comfortable.

On the other hand, I proposed a velocity profile using a sigmoid function to achieve a low jerk. 25 is maximum velocity(m/h). A graph bellow shows x:time, y:velocity.
~~~python
def sigmoid_profile(self, x):
    x = x - 12.5
    return (1 / (1 + np.exp(-0.23 * x))) * 25
~~~

![Screencast](https://github.com/ishota/CarND-Capstone/blob/master/readme_pic/sigmoid_profile.png?raw=true)

## Traffic Light Detector

I used Hough Circle Transform and count circles after masking signal color.

1. Convert image to hsv image
~~~python
def convert_hsv(self, image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
~~~

2. Apply hue value mask
- red_lower_mask = [(0,164,160), (10,255,255)]
- red_upper_mask = [(170,164,160), (179,255,255)]
- yellow_mask = [(20,160,160), (40,255,255)]
- green_mask = [(50,164,160), (80,255,255)]

~~~python
def get_red_mask(self, hsv):
    red_lower_mask = cv2.inRange(hsv, self.red_lower_mask[0], self.red_lower_mask[1])
    red_upper_mask = cv2.inRange(hsv, self.red_upper_mask[0], self.red_upper_mask[1])
    mask = red_lower_mask | red_upper_mask
    return mask

def get_yellow_mask(self, hsv):
    return cv2.inRange(hsv, self.yellow_mask[0], self.yellow_mask[1])

def get_green_mask(self, hsv):
    return cv2.inRange(hsv, self.green_mask[0], self.green_mask[1])
~~~
3. FInd circles in msked image.
I use cv2.HoughCircles function.

4. Classify a signal color
The number of circles was used as the classification criterion.
~~~python
def get_answer(self, rcount, ycount, gcount):

    if rcount == 0 and ycount == 0 and gcount == 0:
        return 'UNKNOWN'

    if rcount > ycount and rcount > gcount:
        return 'RED'

    if ycount > rcount and ycount > gcount:
        return 'YELLOW'

    if gcount > rcount and gcount > ycount:
        return 'GREEN'

    return 'UNKNOWN'
~~~

### Detected result

You can see other result at tfl_imgs/result/*.

![Screencast](https://github.com/ishota/CarND-Capstone/blob/master/tfl_imgs/result/GREEN_8.png?raw=true)
![Screencast](https://github.com/ishota/CarND-Capstone/blob/master/tfl_imgs/result/YELLOW_39.png?raw=true)
![Screencast](https://github.com/ishota/CarND-Capstone/blob/master/tfl_imgs/result/RED_38.png?raw=true)

## Result

The car dtect signal and stopped at low jerk in the Udacity simulator.

![Screencast](https://github.com/ishota/CarND-Capstone/blob/master/gif/stop_line.gif?raw=true)

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the "uWebSocketIO Starter Guide" found in the classroom (see Extended Kalman Filter Project lesson).

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |

We are working on a fix to line up the OpenCV versions between the two.

### Compiling

If you get error of dbw_mkz_msgs, run the following commands
```
sudo apt-get update
sudo apt-get install -y ros-kinetic-dbw-mkz-msgs
cd /home/workspace/CarND-Capstone/ros
rosdep install --from-paths src --ignore-src --rosdistro=kinetic -y
```