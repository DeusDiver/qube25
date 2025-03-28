import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package directory for qube_bringup
    package_dir = get_package_share_directory("qube_bringup")
    
    # Get the package directory for qube_driver (the package with the launch file you want to include)
    driver_package_dir = get_package_share_directory("qube_driver")
    
    # Path to the Xacro file in qube_bringup
    xacro_file = os.path.join(package_dir, "urdf", "controlled_qube.urdf.xacro")
    if not os.path.exists(xacro_file):
        raise FileNotFoundError(f"Xacro file not found: {xacro_file}")
    
    # Process the Xacro file into a URDF string
    robot_description_content = xacro.process_file(xacro_file).toxml()
    
    # Robot State Publisher node
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}]
    )
    
    # RViz node with configuration file
    rviz_config_file = os.path.join(package_dir, "config", "view_config.rviz")
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )
    
    # Include the launch file from qube_driver's launch folder
    driver_launch_file = os.path.join(driver_package_dir, "launch", "qube_driver.launch.py")
    include_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(driver_launch_file)
    )
    
    return LaunchDescription([
        node_robot_state_publisher,
        node_rviz,
        include_driver_launch
    ])
