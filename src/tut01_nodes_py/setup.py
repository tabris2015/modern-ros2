# Copyright 2026 Jose Laruta
from setuptools import find_packages, setup

package_name = 'tut01_nodes_py'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jose Laruta',
    maintainer_email='eduardo.laruta@gmail.com',
    description='Lesson 01: the talker and listener as a pure Python package',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    # ros2 run finds these under install/tut01_nodes_py/lib/tut01_nodes_py/
    entry_points={
        'console_scripts': [
            'talker = tut01_nodes_py.talker:main',
            'listener = tut01_nodes_py.listener:main',
        ],
    },
)
