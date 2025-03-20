import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package directory
    package_dir = get_package_share_directory("qube_bringup")

    # Path to the Xacro file
    xacro_file = os.path.join(package_dir, "urdf", "controlled_qube.urdf.xacro")

    # Ensure the Xacro file exists
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

    # Return the launch description
    return LaunchDescription([
        node_robot_state_publisher,
        node_rviz
    ])
