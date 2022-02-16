# actor avoid   
## Content   
### A) Briefing   
### B) Explanation of the Code   
### C) Reference   
## Briefing
First open up a terminal and input the code   
```python
roslaunch deepexpress_gazebo avoid.launch
```   
This should open up a simulation containing an actor and 4 cafe tables in the gazebo world.   

## Explanation of the Code   
This world contains a world file and a launch file.   
Both the world and the launch file is called *'avoid'*.   
avoid.world can be found in deepexpress_gazebo/world/ and the launch file can be found in deepexpress/launch/   

The world file begins with the necessary conditions for the world 'ground_plane' and 'sun'   

```<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <gui>
      <camera name="user_camera">
        <pose>0 -18 8.0 0 0.523 1.5707</pose>
      </camera>
    </gui>
    <light name="sun" type="directional">
      <cast_shadows>1</cast_shadows>
      <pose>0 0 10 0 -0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>0 0.5 -0.9</direction>
    </light>

    <light name="point_light" type="point">
      <pose>0 -0.377195 6.59868 0 -0 0</pose>
      <diffuse>0.784314 0.784314 0.784314 1</diffuse>
      <specular>0.0980392 0.0980392 0.0980392 1</specular>
      <attenuation>
        <range>50</range>
        <constant>0.8</constant>
        <linear>0</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <cast_shadows>0</cast_shadows>
      <direction>0 0 -1</direction>
    </light> 
  ```
    
The gui part is the adjustment of the camera angle so that the observer can watch the simulation from a certain position.   

Now, the code continues including the important ground_plane and cafe_table as the obstacles for the actors.   

```<include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <name>obstacle1</name>
      <pose>0.5 -1.6 0.2 0 0 0</pose>
      <uri>model://cafe_table</uri>
    </include>

    <include>
      <name>obstacle2</name>
      <pose>2.4 -5.5 0.2 0 0 0</pose>
      <uri>model://cafe_table</uri>
    </include>

    <include>
      <name>obstacle3</name>
      <pose>-1.5 -5.5 0.2 0 0 0</pose>
      <uri>model://cafe_table</uri>
    </include>

    <include>
      <name>obstacle4</name>
      <pose>2.4 -9 0.2 0 0 0</pose>
      <uri>model://cafe_table</uri>
    </include>
  ```
     
Finally we will spawn the actor with an animation walk.dae and a plugin that will avoid any obstacles in the world.

 ```<actor name="actor1">
      <pose>0 3 1.25 0 0 0</pose>
      <skin>
        <filename>walk.dae</filename>
        <scale>1.0</scale>
      </skin>
      <animation name="walking">
        <filename>walk.dae</filename>
        <scale>1.000000</scale>
        <interpolate_x>true</interpolate_x>
      </animation>
      <plugin name="actor_plugin" filename="libActorPlugin.so">
        <target>0 -9 1.24</target>
        <target_weight>1.15</target_weight>
        <obstacle_weight>1.8</obstacle_weight>
        <animation_factor>5.1</animation_factor>
        <ignore_obstacles>
          <model>cafe</model>
          <model>ground_plane</model>
        </ignore_obstacles>
      </plugin>
      <plugin name="actor_ground_state" filename="libgazebo_ros_p3d.so">
        <alwaysOn>true</alwaysOn>
        <updateRate>100.0</updateRate>
        <bodyName>Spine</bodyName>
        <topicName>actor01_odometry_spine</topicName>
        <gaussianNoise>0.01</gaussianNoise>
        <frameName>world</frameName>
        <xyzOffsets>0 0 0</xyzOffsets>
        <rpyOffsets>0 0 0</rpyOffsets>
        <odometryTopic>actor1</odometryTopic>
        <odometryFrame>actor1</odometryFrame>
        <odometryRate>30</odometryRate>
      </plugin>
    </actor>
``` 
##Reference
1) http://gazebosim.org/tutorials?tut=actor&cat=build_robot
