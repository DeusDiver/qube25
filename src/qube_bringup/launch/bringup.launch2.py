import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def launch_setup(context, *args, **kwargs):
    # Resolve substitutions within the provided context
    baud_rate_value = LaunchConfiguration('baud_rate').perform(context)
    simulation_value = LaunchConfiguration('simulation').perform(context)
    device_value = LaunchConfiguration('device').perform(context)
    
    # Get package directory for qube_bringup
    package_dir = get_package_share_directory("qube_bringup")
    xacro_file = os.path.join(package_dir, "urdf", "controlled_qube.urdf.xacro")
    if not os.path.exists(xacro_file):
        raise FileNotFoundError(f"Xacro file not found: {xacro_file}")
    
    # Process the xacro file with the resolved mappings
    robot_description_content = xacro.process_file(
        xacro_file,
        mappings={
            "baud_rate": baud_rate_value,
            "simulation": simulation_value,
            "device": device_value
        }
    ).toxml()

    # Create your nodes
    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}]
    )

    rviz_config_file = os.path.join(package_dir, "config", "view_config.rviz")
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file]
    )

    # Include launch file from qube_driver package
    driver_package_dir = get_package_share_directory("qube_driver")
    driver_launch_file = os.path.join(driver_package_dir, "launch", "qube_driver.launch.py")
    include_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(driver_launch_file)
    )

    return [
        node_robot_state_publisher,
        node_rviz,
        include_driver_launch
    ]

def generate_launch_description():
    # Declare launch arguments
    baud_rate_arg = DeclareLaunchArgument('baud_rate', default_value='115200')
    simulation_arg = DeclareLaunchArgument('simulation', default_value='false')
    device_arg = DeclareLaunchArgument('device', default_value='/dev/ttyUSB1')

    # OpaqueFunction defers processing until the launch context is available
    return LaunchDescription([
        baud_rate_arg,
        simulation_arg,
        device_arg,
        OpaqueFunction(function=launch_setup)
    ])
