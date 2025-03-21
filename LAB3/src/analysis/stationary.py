'''
parse binary data and extract:
Plot time series of each axis, of each measurement. 3 trajectories (x,y,z) per measurement(gyro, accel, mag, euler angles)
Calculate the mean and median the orientation time series data and use a series of
histograms (X, Y, Z) to plot the sensor output distribution around the median. What
type of distribution(s) to you get?
'''
import rosbag2_py
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
import rclpy.serialization
import rosbag2_py
from imu_msg.msg import ImuMsg
import rclpy

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


def quat_to_euler(q):
    r = R.from_quat(q)
    return r.as_euler('xyz', degrees=True)

def plot_timeseries(data, timestamps):
    """Plot time series data for all measurements."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 20))
    axes = axes.flatten()
    
    # convert timestamps to seconds
    t = (np.array(timestamps) - timestamps[0]) / 1e9
    
    # plot Gyro data
    axes[0].plot(t, data['gyro'][:, 0], 'r-', label='X')
    axes[0].plot(t, data['gyro'][:, 1], 'g-', label='Y')
    axes[0].plot(t, data['gyro'][:, 2], 'b-', label='Z')
    axes[0].set_title('Gyroscope Data')
    axes[0].set_ylabel('Angular Velocity (rad/s)')
    axes[0].legend()
    axes[0].grid(True)
    
    # plot Accelerometer data
    axes[1].plot(t, data['accel'][:, 0], 'r-', label='X')
    axes[1].plot(t, data['accel'][:, 1], 'g-', label='Y')
    axes[1].plot(t, data['accel'][:, 2], 'b-', label='Z')
    axes[1].set_title('Accelerometer Data')
    axes[1].set_ylabel('Acceleration (m/s²)')
    axes[1].legend()
    axes[1].grid(True)
    
    # plot Magnetometer data
    axes[2].plot(t, data['mag'][:, 0], 'r-', label='X')
    axes[2].plot(t, data['mag'][:, 1], 'g-', label='Y')
    axes[2].plot(t, data['mag'][:, 2], 'b-', label='Z')
    axes[2].set_title('Magnetometer Data')
    axes[2].set_ylabel('Magnetic Field (Tesla)')
    axes[2].legend()
    axes[2].grid(True)
    
    # convert quaternions to Euler angles and plot
    euler_angles = np.array([quat_to_euler(q) for q in data['orient']])
    axes[3].plot(t, euler_angles[:, 0], 'r-', label='Roll')
    axes[3].plot(t, euler_angles[:, 1], 'g-', label='Pitch')
    axes[3].plot(t, euler_angles[:, 2], 'b-', label='Yaw')
    axes[3].set_title('Orientation (Euler Angles)')
    axes[3].set_ylabel('Angle (degrees)')
    axes[3].set_xlabel('Time (s)')
    axes[3].legend()
    axes[3].grid(True)
    
    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95]) 
    fig.subplots_adjust(hspace=0.4) 
    # plt.savefig('timeseries_plots.png')

def plot_orientation_histograms(data):
    """Plot histograms of orientation data."""
    euler_angles = np.array([quat_to_euler(q) for q in data['orient']])
    medians = np.median(euler_angles, axis=0)
    means = np.mean(euler_angles, axis=0)
    stds = np.std(euler_angles, axis=0)

    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    titles = ['Roll', 'Pitch', 'Yaw']
    
    for i, (ax, title) in enumerate(zip(axes, titles)):
        ax.hist(euler_angles[:, i], bins=50, density=True)
        ax.axvline(medians[i], color='r', linestyle='--', label=f'Median: {medians[i]:.2f}°')
        ax.axvline(means[i], color='g', linestyle='--', 
                  label=f'Mean: {means[i]:.2f}°\nStd: {stds[i]:.2f}°')        
        ax.set_title(f'{title} Distribution')
        ax.set_xlabel('Angle (degrees)')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True)
    
    plt.tight_layout()
    # plt.savefig('orientation_histograms.png')
    print("\nOrientation Statistics:")
    print(f"Means (Roll, Pitch, Yaw): {means}")
    print(f"Medians (Roll, Pitch, Yaw): {medians}")
    print(f"Standard Deviations (Roll, Pitch, Yaw): {stds}")



if __name__ == "__main__":
    bag_path = "/home/savannah/EECE5554/LAB3/src/data/stationary/stationary_0.db3"
    imu_messages = read_data(bag_path)
    rclpy.init()
    # print("First 5 entries of each measurement:")
    # print("Orientation:", imu_messages['orient'][:5])
    # print("Gyroscope:", imu_messages['gyro'][:5])
    # print("Accelerometer:", imu_messages['accel'][:5])
    # print("Magnetometer:", imu_messages['mag'][:5])
    # print("Timestamps:", imu_messages['stamps'][:5])
    rclpy.shutdown()
    
    imu_messages = read_data(bag_path)
    rclpy.init()
    plot_timeseries(imu_messages, imu_messages['stamps'])
    plot_orientation_histograms(imu_messages)
    
    plt.show() 
    rclpy.shutdown()