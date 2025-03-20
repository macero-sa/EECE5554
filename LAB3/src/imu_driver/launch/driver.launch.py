from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    port_arg = DeclareLaunchArgument(
        'port',
        default_value='/dev/pts/4',
        description='Port for VN-100'
    )

    imu_node = Node(
        package='imu_driver',
        executable='driver',
        name='imu_driver',
        parameters=[{
            'port': LaunchConfiguration('port')
        }],
        output='screen'
    )

    return LaunchDescription([
        port_arg,
        imu_node
    ]) 