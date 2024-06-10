# Controlling-Robot-using-Web-Interface

## 1.1 Aim
The goal of this project is to control a robot using a web interface. The robot will move forward
until it encounters an obstacle within 10 cm and stops. The web interface will display the distance
to the obstacle and the distance traveled by each wheel. Additional functionalities include
moving the robot backward and turning at a random angle. When the robot has stopped the website should indicate the distance from the obstacle as well as
the distance traveled by each wheel and uncheck the control box used to start the movement.
Using another control box it should now execute a second script that will move the robot backward 20cm and turn
a random angle, then call the first script again to move until encountering an object.
Use a third control box it initiates a random movement by continuously initiating scripts one and
two until the control box is unchecked (the current script will be finished then and no new one
initiated) During the movement output the distance travelled by each wheel and the distance
from the object stopped at on the webpage (one line per movement).

![ET1](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/4bf3b09a-b49b-4898-a2db-0ce2b3f27d87)


## 1.2 Methodology:
### 1.2.1 Web Interface
Created an HTML page with checkboxes to control the robot’s movements.  

![HTML page](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/a6512a7f-ccdc-402e-9d94-150a39f5edb1)


### 1.2.2 Node.js Server:
Set up a Node.js server to serve the web page and handle WebSocket connections.

### 1.2.3 Python Scripts and result:
#### 1. move forward.py:    
Moves the robot forward until an obstacle is detected within 10 cm,
then stops.

#### Result:  
Initiating ET1’s forward movement triggered from the index.html page using a
checkbox.

![TASK1 1](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/e777ca3a-e666-4f48-aec6-ec0f883addfe)  

![TASK1 2](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/de243597-af06-417a-8528-e7d82580369c)



#### 2. move backward.py:  
Moves the robot backward for 20 cm, then turns at a random angle.  
#### Result:  
Initiating ET1’s backward 20cm movement and turning at a random angle, then
by running first script again unit encountering an object.
![TASK 2 1](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/c8436e0f-d659-4dcc-9c5f-e999a478879b)  

![TASK 2 2](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/5f4183f7-e1ae-4fcf-903e-18ec67117777)



#### 3. random movement.py:  
In this task, we are implementing a control mechanism for a
robotic system that simulates random movement. The system consists of three control
boxes that manage the execution of two scripts to initiate and control the movement of
the robot. The goal is to continuously initiate the robot’s movement through these scripts,
stopping only when the third control box is unchecked. Additionally, during the movement, we will capture and display the distance traveled by each wheel and the distance
from the object the robot stops at, presenting this data on a webpage.

#### Result:  
we create a control mechanism for a robot to simulate random movement using three
control boxes and two scripts. The robot moves continuously until the third control box is
unchecked. We capture and display the distance each wheel travels and the distance from the
object the robot stops at on a webpage.  

![TASK 3 1](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/029a3c6b-1296-4180-a719-454a7fbcc610)


  ![TASK 3 2](https://github.com/Avanindra26/Controlling-Robot-using-Web-Interface/assets/30585056/53a1b480-4b27-4140-9878-60a097f9689c)










