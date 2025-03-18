from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro  # Importer xacro

def generate_launch_description():
    # Hent pakkens sti
    package_dir = get_package_share_directory("qube_description")

    # Prosesser URDF med xacro (endre filnavn til .xacro)
    xacro_file = os.path.join(package_dir, "urdf", "qube.urdf.xacro")  # Endret her
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}]
    )

    # RViz med konfigurasjonsfil
    rviz_config_file = os.path.join(package_dir, "config", "view_config.rviz")
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )

    # Joint State Publisher GUI
    node_joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen"
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_rviz,
        node_joint_state_publisher_gui
    ])