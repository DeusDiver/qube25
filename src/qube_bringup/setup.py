from setuptools import find_packages, setup

package_name = 'qube_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name + '/launch', ['launch/bringup.launch.py']),
    ('share/' + package_name + '/launch', ['launch/bringup.launch2.py']),
    ('share/' + package_name + '/urdf', ['urdf/controlled_qube.urdf.xacro']),
    ('share/' + package_name, ['package.xml']),
],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oliver',
    maintainer_email='olivers.gundersen@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
