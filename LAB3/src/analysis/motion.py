import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rosbag2_py
import rclpy
import rclpy.serialization
from imu_msg.msg import ImuMsg

def read_data(bag_path):

    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions()
    reader.open(storage_options, converter_options)
    available_topics = reader.get_all_topics_and_types()

    print(f"Available topics: {available_topics}", [topic.name for topic in available_topics])

    # initialize data dictionary
    imu_data = {'gyro': [], 'accel': [], 'orient': [], 'mag': [], 'stamps': []}

    # read messages
    while reader.has_next():
        topic, msg_data, timestamp = reader.read_next()
        if topic == "/imu":  
            imu_msg = rclpy.serialization.deserialize_message(msg_data, ImuMsg)
            # extract quaternions
            qx, qy, qz, qw = imu_msg.imu.orientation.x, imu_msg.imu.orientation.y, imu_msg.imu.orientation.z, imu_msg.imu.orientation.w

            # extract gyro
            gyro_x, gyro_y, gyro_z = imu_msg.imu.angular_velocity.x, imu_msg.imu.angular_velocity.y, imu_msg.imu.angular_velocity.z

            # extract accel
            accel_x, accel_y, accel_z = imu_msg.imu.linear_acceleration.x, imu_msg.imu.linear_acceleration.y, imu_msg.imu.linear_acceleration.z

            # extract mag
            mag_x, mag_y, mag_z = imu_msg.mag_field.magnetic_field.x, imu_msg.mag_field.magnetic_field.y, imu_msg.mag_field.magnetic_field.z
            
            imu_data['orient'].append([qx, qy, qz, qw])
            imu_data['gyro'].append([gyro_x, gyro_y, gyro_z])
            imu_data['accel'].append([accel_x, accel_y, accel_z])
            imu_data['mag'].append([mag_x, mag_y, mag_z])
            imu_data['stamps'].append(timestamp)

    imu_data['orient'] = np.array(imu_data['orient'])
    imu_data['gyro'] = np.array(imu_data['gyro'])
    imu_data['accel'] = np.array(imu_data['accel'])
    imu_data['mag'] = np.array(imu_data['mag'])
        

    print(f"Extracted {len(imu_data)} IMU messages")
    return imu_data

'''
from video:
linear motion in z axis t: [04.27 : 46.30]
linear motion in x axis t: [46.48 : 1.17.94]
lin motion in y axis t: [1.18.12 : 1.58.56]
circle in xy ccw(?) t:[1.59.97 : 2.01.38]
circle in yz cw(?) t:[2.03.46 : 2.04.87]
circle in xz[2.11.94 : 2.15.47]
pendelum in xy t: [2.34.97 : 3.02.13]
ctrl c to end bag at t = 3.02.13
video ends at t = 3.05.13
 '''
def plot_3d_motion(data):
    """Plot 3D motion trajectory colored by time."""
    # Convert timestamps to seconds from start
    t = (np.array(data['stamps']) - data['stamps'][0]) / 1e9
    
    # Create color array
    colors = plt.cm.viridis(t/np.max(t))
    
    # Create 3D plots
    fig = plt.figure(figsize=(15, 7))
    
    # Gyroscope 3D plot
    ax1 = fig.add_subplot(121, projection='3d')
    points1 = ax1.scatter(data['gyro'][:, 0], 
                         data['gyro'][:, 1], 
                         data['gyro'][:, 2],
                         c=t, 
                         cmap='viridis')
    ax1.set_title('3D Gyroscope Motion')
    ax1.set_xlabel('X (rad/s)')
    ax1.set_ylabel('Y (rad/s)')
    ax1.set_zlabel('Z (rad/s)')
    
    # Accelerometer 3D plot
    ax2 = fig.add_subplot(122, projection='3d')
    points2 = ax2.scatter(data['accel'][:, 0], 
                         data['accel'][:, 1], 
                         data['accel'][:, 2],
                         c=t, 
                         cmap='viridis')
    ax2.set_title('3D Accelerometer Motion')
    ax2.set_xlabel('X (m/s²)')
    ax2.set_ylabel('Y (m/s²)')
    ax2.set_zlabel('Z (m/s²)')
    
    # Add colorbars
    plt.colorbar(points1, ax=ax1, label='Time (s)')
    plt.colorbar(points2, ax=ax2, label='Time (s)')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    bag_path = "/home/savannah/EECE5554/LAB3/src/data/motion_1/motion_1_0.db3"
    rclpy.init()
    
    # Read all IMU data
    imu_data = read_data(bag_path)
    
    # Plot 3D motion
    plot_3d_motion(imu_data)
    
    rclpy.shutdown()