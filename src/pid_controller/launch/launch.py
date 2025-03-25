import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ✅ Endret bane til riktig config-mappe
    config = os.path.join(
        get_package_share_directory('pid_controller'),
        'config',  # Nå skal filen ligge her riktig
        'parameters.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument('p', default_value='2.0', description='Proportional gain'),
        DeclareLaunchArgument('i', default_value='0.0', description='Integral gain'),
        DeclareLaunchArgument('d', default_value='0.0', description='Derivative gain'),

        Node(
            package='pid_controller',
            executable='pid_final',
            name='pid_controller_node',
            parameters=[{
                'p': LaunchConfiguration('p'),
                'i': LaunchConfiguration('i'),
                'd': LaunchConfiguration('d'),
            }]
        ),
        Node(
            package='joint_simulator',
            executable='joint_simulator_node',
            name='joint_simulator_node',
            parameters=[config]  # ✅ Laster parameters.yaml
        ),
        Node(
            package='py_srvcli',  
            executable='reference_input',
            name='reference_input_node',
        ),
    ])

