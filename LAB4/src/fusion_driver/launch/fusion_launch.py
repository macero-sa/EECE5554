from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([

        DeclareLaunchArgument(
            'gps_port',
            default_value='/dev/pts/16',
            description='Port for the GPS'
        ),
        DeclareLaunchArgument(
            'imu_port',
            default_value='/dev/pts/17',
            description='Port for the IMU'
        ),
        Node(
            package='gps_driver',
            executable='gps_driver',
            name='gps_driver',
            parameters=[{
                'gps_port': LaunchConfiguration('gps_port')
            }],
            output='screen'
        ),
        Node(
            package='imu_driver',
            namespace='imu_driver',
            executable='imu_driver',
            name='imu_driver',
            parameters=[{
                'imu_port': LaunchConfiguration('imu_port')
            }],
            output='screen'
        )
    ])