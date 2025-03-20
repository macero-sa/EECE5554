import rclpy
from rclpy.node import Node
import serial
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from std_msgs.msg import Header
from imu_msg.msg import ImuMsg
import math
from geometry_msgs.msg import Quaternion
import numpy as np


class Driver(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        # self.declare_parameter('frame_id', '“IMU1_Frame')

        port = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value
        try:
            self.ser = serial.Serial(port, baudrate)
            self.get_logger().info(f'Connected to {port} at {baudrate} baud')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to {port}: {e}')
            raise
        
        self.publisher = self.create_publisher(ImuMsg, '/imu', 10)
        self.timer = self.create_timer(1.0 / 4.0, self.pub_imu_data)

    def pub_imu_data(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if not line:
                return
            
            fields = line.split(',')
            yaw, pitch, roll = map(math.radians, map(float, fields[1:4])) # math needs radians for quaternion compute
            mag_x, mag_y, mag_z = map(float, fields[4:7])
            acc_x, acc_y, acc_z = map(float, fields[7:10])
            gyro_x, gyro_y, gyro_z = map(float, fields[10:13])
            # convert yaw pitch roll to quaternions, ref quaternion_to_euler func in ros2 tf docs
            ai = roll/2.0
            aj = pitch/2.0
            ak = yaw/2.0
            ci = math.cos(ai)
            si = math.sin(ai)
            cj = math.cos(aj)
            sj = math.sin(aj)
            ck = math.cos(ak)
            sk = math.sin(ak)
            cc = ci*ck
            cs = ci*sk
            sc = si*ck
            ss = si*sk

            q = np.empty((4, ))
            q[0] = cj*sc - sj*cs
            q[1] = cj*ss + sj*cc
            q[2] = cj*cs - sj*sc
            q[3] = cj*cc + sj*ss
            
            imu_msg = ImuMsg()
            imu_msg.header = Header()
            imu_msg.raw_data = line
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'IMU1_Frame'
            imu_msg.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])
            self.publisher.publish(imu_msg)
 
        except Exception as e:
            self.get_logger().error(f'Error reading or processing from port: {e}')


def main(args=None):
    rclpy.init(args=args)
    imu_driver = Driver()
    rclpy.spin(imu_driver)
    imu_driver.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    