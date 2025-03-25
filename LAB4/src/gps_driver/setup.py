from setuptools import setup
import os
from glob import glob

package_name = 'gps_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py'))
    ],
    install_requires=['setuptools',
                     'pyproj',
                     'rclpy',
                     'pyserial',
                     'utm',
                     ],
    zip_safe=True,
    maintainer='savannahmacero',
    maintainer_email='macero.sa@northeastern.edu',
    description='GPS driver package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gps_driver = gps_driver.gps_driver:main'
        ],
    },
)
