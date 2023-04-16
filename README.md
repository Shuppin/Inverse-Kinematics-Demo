# Inverse Kinematics Demo

Welcome to my Inverse Kinematics Demo! This program demonstrates an inverse kinematics algorithm that allows you to specify the position of an end effector, such as the tip of a robotic arm or the foot in a running animation, and computes the joint angles required to achieve that position. 

> The `main.py` file provides a visual representation of the algorithm in action, while the `iksystem.py` and `arm.py` files are fully modularized and can be used independently in your own projects, just make sure to include both these files in the same directory .

 ---
## Demo
Watch a quick demo of the program in action here:
![demo pending]()

> Note: Video compression may make the arm segments appear to jiggle, but the algorithm is stable and they are not actually jiggling.

---

## Installation

You can either download a prebuilt version of the program by clicking [here (link pending)](), or run the program from source. 

### Running from source 

To run the program from source, follow these simple steps:

1. Open a terminal and clone the repo by running `git clone https://github.com/Shuppin/Inverse-Kinematics-Demo.git` in your terminal.
2. Enter the directory by running `cd Inverse-Kinematics-Demo`
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the program by executing `python src/main.py` in your terminal. 

That's it! You should now be able to use the Inverse Kinematics Demo to compute joint angles for your robotic arm. 
