import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rosbag2_py
import rclpy
import rclpy.serialization
from imu_msg.msg import ImuMsg
from scipy.integrate import cumtrapz
from scipy.signal import butter, filtfilt

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
        

    print(f"Extracted {len(imu_data['stamps'])} IMU messages")
    return imu_data


# z motion ends at 1:05 in video. z motion from t = [0, 65 - 13 = 52]
# x motion t = [53, 60 + 28 - 13 = 75]
# y motion t = [76, 120 + 23 - 13 = 130] 
# heel spin from 2.26 to 2.50: t = [120 + 26 - 13 = 133, 120 + 54 - 13 = 161]
# aggressive circles about y: t = [180 -13 = 167, 177]

def extract_time_window(imu_data, start_time, end_time):
    """Extract IMU data within a specific time window."""
    # Convert time to nanoseconds
    timestamps = np.array(imu_data['stamps'])
    t = (timestamps - timestamps[0]) / 1e9  # Convert to seconds from start
    
    # Create mask for time window
    mask = (t >= start_time) & (t <= end_time)
    
    # Extract data for time window
    extracted_data = {}
    for key, value in imu_data.items():
        if isinstance(value, np.ndarray):
            extracted_data[key] = value[mask]
        else:
            extracted_data[key] = [v for i, v in enumerate(value) if mask[i]]
            
    return extracted_data

def plot_clips(imu_data):
    extracted_data_z = extract_time_window(imu_data, 0, 52)
    extracted_data_x = extract_time_window(imu_data, 53, 75)
    extracted_data_y = extract_time_window(imu_data, 76, 130)
    extracted_data_circle_y = extract_time_window(imu_data, 167, 177)
    
    # time normalization
    t1 = (np.array(extracted_data_z['stamps']) - extracted_data_z['stamps'][0]) / 1e9 
    t2 = (np.array(extracted_data_x['stamps']) - extracted_data_x['stamps'][0]) / 1e9
    t3 = (np.array(extracted_data_y['stamps']) - extracted_data_y['stamps'][0]) / 1e9
    t4 = (np.array(extracted_data_circle_y['stamps']) - extracted_data_circle_y['stamps'][0]) / 1e9

    fig1 = plt.figure(figsize=(10, 8))
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.plot(0 * np.ones_like(extracted_data_z['accel'][:, 0]), 
            0 * np.ones_like(extracted_data_z['accel'][:, 0]), 
            extracted_data_z['accel'][:, 2], 
            label='Linear Motion along Z axis', color='b', marker='o')
    ax1.plot(extracted_data_x['accel'][:, 0], 
            0 * np.ones_like(extracted_data_x['accel'][:, 0]), 
            0 * np.ones_like(extracted_data_x['accel'][:, 0]), 
            label='Linear Motion along X axis', color='g', marker='o')
    ax1.plot(0 * np.ones_like(extracted_data_y['accel'][:, 0]), 
            extracted_data_y['accel'][:, 1], 
            0 * np.ones_like(extracted_data_y['accel'][:, 0]), 
            label='Linear Motion along Y axis', color='r', marker='o')

    ax1.set_xlabel('X (m/s²)')
    ax1.set_ylabel('Y (m/s²)')
    ax1.set_zlabel('Z (m/s²)')
    ax1.set_title('Linear Movements')
    ax1.legend()

    fig2 = plt.figure(figsize=(10, 8))
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.plot(extracted_data_circle_y['accel'][:, 0], 
            0 * np.ones_like(extracted_data_circle_y['accel'][:, 0]), 
            extracted_data_circle_y['accel'][:, 2], 
            label='Circle about Y axis', color='m', marker='o')
    
    ax2.set_xlabel('X (m/s²)')
    ax2.set_ylabel('Y (m/s²)')
    ax2.set_zlabel('Z (m/s²)')
    ax2.set_title('Circular Motion about Y Axis')
    ax2.legend()
    plt.show()

def plot_actual(imu_data):
    """Plot full 3D trajectories for linear motions in separate subplots."""
    # Extract time windows
    extracted_data_z = extract_time_window(imu_data, 0, 52)
    extracted_data_x = extract_time_window(imu_data, 53, 75)
    extracted_data_y = extract_time_window(imu_data, 76, 130)
    
    # Create figure with three subplots
    fig = plt.figure(figsize=(18, 6))
    
    # Plot data for Z-axis motion
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(extracted_data_z['accel'][:, 0],
                extracted_data_z['accel'][:, 1],
                extracted_data_z['accel'][:, 2],
                label='Z-axis Motion', color='b', alpha=0.6)
    ax1.set_title('Linear Motion along Z\nt=[0, 52]s')
    
    # Plot data for X-axis motion
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(extracted_data_x['accel'][:, 0],
                extracted_data_x['accel'][:, 1],
                extracted_data_x['accel'][:, 2],
                label='X-axis Motion', color='g', alpha=0.6)
    ax2.set_title('Linear Motion along X\nt=[53, 75]s')
    
    # Plot data for Y-axis motion
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(extracted_data_y['accel'][:, 0],
                extracted_data_y['accel'][:, 1],
                extracted_data_y['accel'][:, 2],
                label='Y-axis Motion', color='r', alpha=0.6)
    ax3.set_title('Linear Motion along Y\nt=[76, 130]s')
    
    # Set common properties for all subplots
    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel('X (m/s²)')
        ax.set_ylabel('Y (m/s²)')
        ax.set_zlabel('Z (m/s²)')
        ax.legend()
        ax.set_box_aspect([1,1,1])
        ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    bag_path = "/home/savannah/EECE5554/LAB3/src/data/motion/motion_0.db3"
    rclpy.init()
    imu_data = read_data(bag_path)
    rclpy.shutdown()
    plot_clips(imu_data)
    plot_actual(imu_data)
