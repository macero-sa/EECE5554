import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import Imu, MagneticField
import matplotlib.pyplot as mlp
import pandas as pds
import sqlite3
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import struct
import numpy as np
from scipy.spatial.transform import Rotation as R

# Define the bag path
bag_path = "/home/buchalterl/EECE5554/LAB4/data/data_going_in_circles/data_going_in_circles.db3"
imu_msg_type = get_message('msg_combined/msg/IMUmsg')
connection = sqlite3.connect(bag_path)

prompt = """
SELECT messages.data FROM messages
JOIN topics ON messages.topic_id = topics.id
WHERE topics.name = '/imu'
"""

data = pds.read_sql_query(prompt,connection)
connection.close()

time = []
gyrox = []
gyroy = []
gyroz = []
accx = []
accy = []
accz = []
magx = []
magy = []
magz = []
Eulerx = []
Eulery = []
Eulerz = []

for _, row in data.iterrows():
    bytes = row["data"]
    msg = deserialize_message(bytes,imu_msg_type)
    t = msg.header.stamp.sec + msg.header.stamp.nanosec*1e-9
    time.append(t)

    xgyro = msg.imu.angular_velocity.x
    ygyro = msg.imu.angular_velocity.y
    zgyro = msg.imu.angular_velocity.z
    xacc = msg.imu.linear_acceleration.x
    yacc = msg.imu.linear_acceleration.y
    zacc = msg.imu.linear_acceleration.z
    xmag = msg.mag_field.magnetic_field.x
    ymag = msg.mag_field.magnetic_field.y
    zmag = msg.mag_field.magnetic_field.z
    qx = msg.imu.orientation.x
    qy = msg.imu.orientation.y
    qz = msg.imu.orientation.z
    qw = msg.imu.orientation.w

    gyrox.append(xgyro)
    gyroy.append(ygyro)
    gyroz.append(zgyro)
    accx.append(xacc)
    accy.append(yacc)
    accz.append(zacc)
    magx.append(xmag)
    magy.append(ymag)
    magz.append(zmag)
    quaternion = [qx, qy, qz, qw]
    r = R.from_quat(quaternion)
    Euler = r.as_euler('xyz', degrees=True)
    Eulerx.append(Euler[0])
    Eulery.append(Euler[1])
    Eulerz.append(Euler[2])

time = np.array(time)  
time = time - time[0]
Eulerx = np.array(Eulerx)
Eulery = np.array(Eulery)
Eulerz = np.array(Eulerz)
magx = np.array(magx)
magy = np.array(magy)
magz = np.array(magz)
gyrox = np.array(gyrox)
gyroy = np.array(gyroy)
gyroz = np.array(gyroz)
accx = np.array(accx)
accy = np.array(accy)
accz = np.array(accz)

#Plotting Accelerometer
fig, axes = mlp.subplots(1, 3, figsize=(16, 6), sharex=True)
# Plot Acc X
axes[0].plot(time, accx, 'r')
axes[0].set_title("Accelerometer X")
axes[0].set_ylabel("Acceleration (m/s^2)")
axes[0].set_xlabel("Time (s)")
# Plot Acc Y
axes[1].plot(time, accy, 'g')
axes[1].set_title("Accelerometer Y")
axes[1].set_xlabel("Time (s)")
# Plot Acc Z
axes[2].plot(time, accz, 'b')
axes[2].set_title("Accelerometer Z")
axes[2].set_xlabel("Time (s)")
# Adjust layout
mlp.tight_layout()
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)
mlp.show()

#Plotting Gyro
fig, axes = mlp.subplots(1, 3, figsize=(16, 6), sharex=True)
# Plot Gyro X
axes[0].plot(time, gyrox, 'r')
axes[0].set_title("Gyro X")
axes[0].set_ylabel("Angular Velocity (deg/s)")
axes[0].set_xlabel("Time (s)")
# Plot Gyro Y
axes[1].plot(time, gyroy, 'g')
axes[1].set_title("Gyro Y")
axes[1].set_xlabel("Time (s)")
# Plot Gyro Z
axes[2].plot(time, gyroz, 'b')
axes[2].set_title("Gyro Z")
axes[2].set_xlabel("Time (s)")
# Adjust layout
mlp.tight_layout()
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)
mlp.show()

#Plotting Mag
fig, axes = mlp.subplots(1, 3, figsize=(16, 6), sharex=True)
# Plot Mag X
axes[0].plot(time, magx, 'r')
axes[0].set_title("Magnetometer X")
axes[0].set_ylabel("Magnetic Field (Gauss)")
axes[0].set_xlabel("Time (s)")
# Plot Mag Y
axes[1].plot(time, magy, 'g')
axes[1].set_title("Magnetometer Y")
axes[1].set_xlabel("Time (s)")
# Plot Mag Z
axes[2].plot(time, gyroz, 'b')
axes[2].set_title("Magnetometer Z")
axes[2].set_xlabel("Time (s)")
# Adjust layout
mlp.tight_layout()
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)
mlp.show()

#Plotting Orientation
fig, axes = mlp.subplots(1, 3, figsize=(16, 6), sharex=True)
# Plot Orientation X
axes[0].plot(time, Eulerx, 'r')
axes[0].set_title("Orientation Roll (X)")
axes[0].set_ylabel("Angle (deg)")
axes[0].set_xlabel("Time (s)")
# Plot Orientation Y
axes[1].plot(time, Eulery, 'g')
axes[1].set_title("Orientation Pitch (Y)")
axes[1].set_xlabel("Time (s)")
# Plot Orientation Z
axes[2].plot(time, Eulerz, 'b')
axes[2].set_title("Orientation Yaw (Z)")
axes[2].set_xlabel("Time (s)")
# Adjust layout
mlp.tight_layout()
axes[0].grid(True)
axes[1].grid(True)
axes[2].grid(True)
mlp.show()

