#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Hent pakkemappa
    qube_driver_share = get_package_share_directory('qube_driver')
    qube_bringup_share = get_package_share_directory('qube_bringup')
    
    # Inkluder qube_driver sin launch-fil
    qube_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(qube_driver_share, 'launch', 'qube_driver.launch.py')
        )
    )
    
    # RViz-konfigurasjon (lag ei rviz config-fil i config/ mappa om nødvendig)
    rviz_config = os.path.join(qube_bringup_share, 'config', 'controlled_qube.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )
    
    # Prosesser controlled_qube.urdf.xacro for å få robot_description
    controlled_urdf = os.path.join(qube_bringup_share, 'urdf', 'controlled_qube.urdf.xacro')
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command([
                'xacro ', controlled_urdf,
                ' baud_rate:=115200',
                ' device:=/dev/ttyUSB0',
                ' simulation:=false'
            ])
        }]
    )
    
    return LaunchDescription([
        qube_driver_launch,
        rviz_node,
        robot_state_publisher_node
    ])
