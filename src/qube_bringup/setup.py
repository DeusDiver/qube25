from setuptools import find_packages, setup
import os
from glob import glob  # Don't forget to import glob

package_name = 'qube_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        # Inkluder alle launch filer
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # Inkluder alle URDF filer
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf.xacro')),
        # Inkluder alle config filer
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oliver',
    maintainer_email='olivers.gundersen@gmail.com',
    description='Qube robot bringup package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)