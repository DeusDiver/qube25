import os
import xacro  # <-- Missing import added
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def launch_setup(context, *args, **kwargs):
    # Get package directories
    qube_bringup_dir = get_package_share_directory("qube_bringup")
    qube_driver_dir = get_package_share_directory("qube_driver")

    # Process Xacro file with substitutions
    xacro_file = os.path.join(qube_bringup_dir, "urdf", "controlled_qube.urdf.xacro")
    robot_description = xacro.process_file(
        xacro_file,
        mappings={
            "baud_rate": LaunchConfiguration("baud_rate").perform(context),
            "simulation": LaunchConfiguration("simulation").perform(context),
            "device": LaunchConfiguration("device").perform(context),
        }
    ).toxml()

    # Robot State Publisher Node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # Joint State Publisher GUI
    node_joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        output="screen"
    )


    # RViz Node
    rviz_config = os.path.join(qube_bringup_dir, "config", "view_config.rviz")
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config]
    )

    # Include Qube Driver Launch
    qube_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(qube_driver_dir, "launch", "qube_driver.launch.py")
        ])
    )

    return [
        robot_state_publisher,
        rviz_node,
        qube_driver_launch,
        node_joint_state_publisher_gui
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("baud_rate", default_value="115200"),
        DeclareLaunchArgument("simulation", default_value="false"),
        DeclareLaunchArgument("device", default_value="/dev/ttyUSB0"),
        OpaqueFunction(function=launch_setup)
    ])