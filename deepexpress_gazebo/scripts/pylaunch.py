#!/usr/bin/env python

import subprocess
import sys
import time
import roslaunch
import rospy

state = False

class Node:
    def __init__(self, name_arg, package_arg, executable_arg, instance_arg):
        self._name = name_arg
        self._package = package_arg
        self._executable = executable_arg
        self._instance_num = instance_arg

        self._launch = roslaunch.scriptapi.ROSLaunch()
        self._process = None
        self._node = None

    def define_node(self):
        self._node = roslaunch.core.Node(package=self._package, node_type=self._executable, name=self._name, namespace='/',
                                         machine_name=None, args=str(self._instance_num),
                                         respawn=False, respawn_delay=0.0,
                                         remap_args=None, env_args=None, output='screen', cwd=None,
                                         launch_prefix=None, required=False, filename='<unknown>')

    def launch(self):
        self._launch.start()
        self._process = self._launch.launch(self._node)

    def kill(self):
        self._process.stop()

    def status(self):
        if self._process.is_alive():
            return "Active"
        else:
            return "Inactive"


def launch_core():
    subprocess.Popen('roscore')
    time.sleep(60)  # Delay to initialize the roscore


def launch_sim():
    package = 'deepexpress_gazebo'
    executable = 'simulation.launch'
    node = roslaunch.core.Node(package, executable)

    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    launch.launch(node)

def main(number_of_nodes):
    # List to perform operations on a node
    node_collections = []

    try:
        launch_core()
        global state
        launch_sim()

        package = 'deepexpress_description'
        executable = 'box1.urdf'

        # For given number of instances
        for i in range(1, number_of_nodes+1):
            name = 'Turtle' + str(i)
            node_collections.append(Node(name_arg=name,
                                         package_arg=package,
                                         executable_arg=executable,
                                         instance_arg=i))

            # Define Nodes
            node_collections[-1].define_node()

            # Launch Nodes
            node_collections[-1].launch()

        rospy.set_param('/activity_status', 1)

        while True:
            status = rospy.get_param('/activity_status')

            if status != 1:
                break

    except KeyboardInterrupt:
        state = True
        print("Keyboard Interrupt", state)

    except Exception as error:
        print(error)

    finally:
        print("Exiting the process ....")
        # Don't need to Kill nodes explicitly since 
        # they died when rospy.is_shutdown interrupt occurred
        sys.exit()

if __name__ == '__main__':
    main(int(sys.argv[1]))