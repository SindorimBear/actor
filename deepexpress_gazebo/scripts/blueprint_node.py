#!/usr/bin/env python
"""
Blueprint node for launching using ROS APIs
Author: Shilpaj Bhalerao
Date: Oct 04, 2020
"""
import math
import random
import sys
from turtle import Turtle
import tf
import rospy
from std_msgs.msg import Int64


class Instance:
    """
    Class for multiple instance launch
    """
    def __init__(self, value):
        # Initialize a node
        rospy.init_node('turtle', anonymous=False)

        # Log node status
        rospy.loginfo("Node Initialized: Turtle"+str(value))

        # Private variable for the number of instance
        self._instance_number = value

        # Broadcaster
        self.broadcast = tf.TransformBroadcaster()

        # Variables for position and orientation of turtles
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.theta = 0.0

        # Rate
        self.rate = rospy.Rate(10.0)

        # Object of a Turtle class to interact with turtles
        self.turtle = None

        # Spawn turtles randomly
        self.random_spawn()

        # Initiate topic for instance and publisher to publish data
        topic_name = '/Node' + str(self._instance_number) + '/topic' + str(self._instance_number)
        self.pub = rospy.Publisher(topic_name, Int64, queue_size=1)

        while not rospy.is_shutdown():
            # Broadcast tf
            self.dynamic_frame()

            # Publish data
            self.pub.publish(self._instance_number)
            self.rate.sleep()

    def random_spawn(self):
        """
        Method to spawn only a single instance of a turtle
        """
        self.turtle = Turtle(self._instance_number)

        self.rand_pos()

        self.turtle.spawn(self.x_pos, self.y_pos, self.theta)
        print(self.turtle.get_name())

    def random_spawn_test(self):
        """
        Method to spawn multiple instances of a turtle
        """
        collection = []
        for i in range(self._instance_number):
            collection.append(Turtle(i))

            self.rand_pos()

            collection[i].spawn(self.x_pos, self.y_pos, self.theta)
            print(collection[i].get_name())

    def rand_pos(self):
        """
        Method to set a random position and orientation of a turtle in a turtlesim
        """
        self.x_pos = random.randint(0, 11)
        self.y_pos = random.randint(0, 11)
        self.theta = random.random()

    def dynamic_frame(self):
        """
        Method to broadcast the dynamic transform
        """
        time_now = rospy.Time.now().to_sec() * math.pi
        self.broadcast.sendTransform((2.0 * math.sin(time_now), 2.0 * math.cos(time_now), 0.0),
                                     (0.0, 0.0, 0.0, 1.0),
                                     rospy.Time.now(),
                                     "turtle" + str(self._instance_number),
                                     "world")


def on_exit():
    """
    Sequence to be executed during shutdown
    """
    rospy.set_param('/activity_status', 0)


def main(value):
    """
    Main Function
    """
    try:
        # reset_sim()
        Instance(value)
        rospy.on_shutdown(on_exit)
    except Exception as error:
        print(error)
        sys.exit()


if __name__ == '__main__':
    main(int(sys.argv[1]))