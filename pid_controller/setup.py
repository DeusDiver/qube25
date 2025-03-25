from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'pid_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ✅ Beholder eksisterende launch-fil inkludering
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # ✅ Legger til YAML-filen slik at den blir installert riktig
        (os.path.join('share', package_name, 'config'), glob('launch/config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oliver',
    maintainer_email='oliver@todo.todo',
    description='ROS2 PID Controller Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pid_node = pid_controller.pid_controller_node:main',
            'test_listen = pid_controller.publish_test:main',
            'pid_final = pid_controller.pid_controller_node_2:main',
            'ref_input = pid_controller.reference_input_node:main'  # ✅ Beholder reference_input_node
        ],
    },
)

