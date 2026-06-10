from setuptools import find_packages, setup

package_name = 'pendulum_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vishwesh',
    maintainer_email='vishweshpatil2110@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
   entry_points={
    'console_scripts': [
        'pendulum_publisher = pendulum_controller.pendulum_publisher:main',
        'pendulum_subscriber = pendulum_controller.pendulum_subscriber:main',
        'pendulum_balance = pendulum_controller.pendulum_balance:main',
        'gazebo_balance = pendulum_controller.gazebo_balance:main',
    ],
},
)
