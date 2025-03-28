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

# Define the bag path
bag_path = "/home/buchalterl/EECE5554/LAB4/data/data_driving/data_driving.db3"
gps_msg_type = get_message('msg_combined/msg/GPSmsg')
connection = sqlite3.connect(bag_path)

prompt = """
SELECT messages.data FROM messages
JOIN topics ON messages.topic_id = topics.id
WHERE topics.name = '/gps'
"""

data = pds.read_sql_query(prompt,connection)
connection.close()

time = []
easting = []
northing = []
altitude = []

for _, row in data.iterrows():
    bytes = row["data"]
    msg = deserialize_message(bytes,gps_msg_type)
    t = msg.utc
    time.append(float(t))

    east = msg.utm_easting
    north = msg.utm_northing
    alt = msg.altitude

    easting.append(east)
    northing.append(north)
    altitude.append(alt)

time = np.array(time)  
easting = np.array(easting)
northing = np.array(northing)
altitude = np.array(altitude)

#Plotting Northing vs. Easting
mlp.xlabel("UTM Easting [m]")
mlp.ylabel("UTM Northing [m]")
mlp.title("UTM Coordinates, Moving")
mlp.scatter(easting,northing,label="Moving Data")
mlp.grid
mlp.legend()
mlp.show()

#Plotting Alt vs. Time
mlp.figure(figsize=(10,10))
mlp.xlabel("Scaled Time [sec]")
mlp.ylabel("Altitude [m]")
mlp.title("Altitude vs Time, Moving")
mlp.scatter(time,altitude,label="Moving Altitude Data")
mlp.grid
mlp.legend()
mlp.show()
