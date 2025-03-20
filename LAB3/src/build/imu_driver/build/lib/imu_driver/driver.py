import rclpy
from rclpy.node import Node
import serial
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from geometry_msgs.msg import Vector3, Quaternion
from std_msgs.msg import Header
from imu_msg.msg import ImuMsg
import math
import numpy as np


class Driver(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)

        port = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value
        try:
            self.ser = serial.Serial(port, baudrate)
            self.get_logger().info(f'Connected to {port} at {baudrate} baud')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to {port}: {e}')
            raise
        
        self.configure_imu()
        self.publisher = self.create_publisher(ImuMsg, '/imu', 10)
        self.timer = self.create_timer(1.0 / 40.0, self.pub_imu_data)

    def pub_imu_data(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if not line:
                return
            
            # self.get_logger().info(f"Raw IMU Data: {line}")

            if not line.startswith("$VNYMR"):
                self.get_logger().warn(f"Unexpected IMU Data: {line}")
                return

            rm_checksum = line.split('*')[0]
            fields = rm_checksum.split(',')

            if len(fields) < 13:  
                self.get_logger().warn(f"Incomplete IMU Data: {line}")
                return
            

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
            imu_msg.raw_data = line            
            imu_msg.header = Header()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'IMU1_Frame'
            imu_msg.imu = Imu()
            
            # imu_msg.imu.angular_velocity = Vector3()
            # imu_msg.imu.angular_velocity.x = gyro_x
            # imu_msg.imu.angular_velocity.y = gyro_y
            # imu_msg.imu.angular_velocity.z = gyro_z
            imu_msg.imu.angular_velocity = Vector3(x=gyro_x, y=gyro_y, z=gyro_z)

            
            # imu_msg.imu.linear_acceleration = Vector3()
            # imu_msg.imu.linear_acceleration.x = acc_x
            # imu_msg.imu.linear_acceleration.y = acc_y
            # imu_msg.imu.linear_acceleration.z = acc_z
            imu_msg.imu.linear_acceleration = Vector3(x=acc_x, y=acc_y, z=acc_z)
            
            imu_msg.mag_field = MagneticField()
            # imu_msg.mag_field.magnetic_field = Vector3()
            # imu_msg.mag_field.magnetic_field.x = mag_x
            # imu_msg.mag_field.magnetic_field.y = mag_y
            # imu_msg.mag_field.magnetic_field.z = mag_z
            imu_msg.mag_field.magnetic_field = Vector3(x=mag_x, y=mag_y, z=mag_z)

        
            # imu_msg.imu.orientation.x = q[0]
            # imu_msg.imu.orientation.y = q[1]
            # imu_msg.imu.orientation.z = q[2]
            # imu_msg.imu.orientation.w = q[3]

            imu_msg.imu.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])
            self.publisher.publish(imu_msg)
 
        except Exception as e:
            self.get_logger().error(f'Error reading or processing from port: {e}')

    def configure_imu(self):
        try:
            # command = b'VNWRG,07,40*59\r\n'
            self.ser.write(b'VNWRG,8,40\r\n')
            self.get_logger().info('Configured to 40 Hz')
            self.ser.write(b'$VNRRG,07\r\n')
            response = self.ser.readline().decode('utf-8').strip()
            self.get_logger().info(f"IMU Output Rate Readback: {response}")
        except Exception as e:
            self.get_logger().error(f'Failed to configure IMU: {e}')
            raise

def main(args=None):
    rclpy.init(args=args)
    imu_driver = Driver()
    rclpy.spin(imu_driver)
    imu_driver.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
