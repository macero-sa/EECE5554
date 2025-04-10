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
from gps_message.msg import GpsMsg
import rclpy

def read_data(bag_path):
    reader = rosbag2_py.SequentialReader()
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions(
        input_serialization_format='cdr',
        output_serialization_format='cdr'
    )
    
    try:
        reader.open(storage_options, converter_options)
    except Exception as e:
        print(f"Error opening bag file: {e}")
        return None, None

    # Initialize counters for debugging
    imu_count = 0
    gps_count = 0
    
    # initialize data dictionary
    imu_data = {'gyro': [], 'accel': [], 'orient': [], 'mag': [], 'imu_stamps': []}
    gps_data = {'lat': [], 'lon': [], 'alt': [], 'northing':[], 'easting': [], 'gps_stamps': []}

    try:
        while reader.has_next():
            topic_name, data, timestamp = reader.read_next()
            
            if topic_name == "/imu":
                imu_count += 1
                imu_msg = rclpy.serialization.deserialize_message(data, ImuMsg)
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
                imu_data['imu_stamps'].append(timestamp)
                
            elif topic_name == "/gps":
                gps_count += 1
                gps_msg = rclpy.serialization.deserialize_message(data, GpsMsg)
                # extract GPS data if needed
                lat = gps_msg.latitude
                lon = gps_msg.longitude
                alt = gps_msg.altitude
                northing = gps_msg.utm_northing
                easting = gps_msg.utm_easting
                gps_data['lat'].append(lat)
                gps_data['lon'].append(lon)
                gps_data['alt'].append(alt)
                gps_data['northing'].append(northing)
                gps_data['easting'].append(easting)
                gps_data['gps_stamps'].append(timestamp)
                
            if imu_count % 1000 == 0 or gps_count % 50 == 0:
                print(f"Processed {imu_count} IMU messages and {gps_count} GPS messages")
                
    except Exception as e:
        print(f"Error reading messages: {e}")
    finally:
        print(f"Final counts - IMU: {imu_count}, GPS: {gps_count}")
        
    # Convert lists to numpy arrays
    for key in imu_data:
        if imu_data[key]:
            imu_data[key] = np.array(imu_data[key])
    
    for key in gps_data:
        if gps_data[key]:
            gps_data[key] = np.array(gps_data[key])

    return imu_data, gps_data


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
    bag_path = '/home/savannah/EECE5554/LAB4/data/data_driving/data_driving_0.db3'
    imu_data, gps_data = read_data(bag_path)
    rclpy.init()

    # Print GPS coordinates
    print("\nGPS Coordinate Statistics:")
    print("-" * 50)
    print("Latitude values:")
    print(f"Min: {np.min(gps_data['lat']):.6f}")
    print(f"Max: {np.max(gps_data['lat']):.6f}")
    print(f"Mean: {np.mean(gps_data['lat']):.6f}")
    
    print("\nLongitude values:")
    print(f"Min: {np.min(gps_data['lon']):.6f}")
    print(f"Max: {np.max(gps_data['lon']):.6f}")
    print(f"Mean: {np.mean(gps_data['lon']):.6f}")
    
    print("\nUTM Easting values (meters):")
    print(f"Min: {np.min(gps_data['easting']):.2f}")
    print(f"Max: {np.max(gps_data['easting']):.2f}")
    print(f"Mean: {np.mean(gps_data['easting']):.2f}")
    
    print("\nUTM Northing values (meters):")
    print(f"Min: {np.min(gps_data['northing']):.2f}")
    print(f"Max: {np.max(gps_data['northing']):.2f}")
    print(f"Mean: {np.mean(gps_data['northing']):.2f}")

    # Create subplots for better visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
    
    # Plot Latitude over time
    time = (np.array(gps_data['gps_stamps']) - gps_data['gps_stamps'][0]) / 1e9
    ax1.plot(time, gps_data['lat'], 'b.')
    ax1.set_title('Latitude vs Time')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Latitude (degrees)')
    ax1.grid(True)

    # Plot Longitude over time
    ax2.plot(time, gps_data['lon'], 'r.')
    ax2.set_title('Longitude vs Time')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Longitude (degrees)')
    ax2.grid(True)

    # Plot UTM coordinates
    ax3.scatter(gps_data['easting'], gps_data['northing'], c=time, cmap='viridis')
    ax3.set_title('UTM Coordinates')
    ax3.set_xlabel('Easting (m)')
    ax3.set_ylabel('Northing (m)')
    ax3.grid(True)
    
    # Plot relative UTM coordinates (centered at first point)
    easting_rel = gps_data['easting'] - gps_data['easting'][0]
    northing_rel = gps_data['northing'] - gps_data['northing'][0]
    ax4.scatter(easting_rel, northing_rel, c=time, cmap='viridis')
    ax4.set_title('Relative UTM Coordinates')
    ax4.set_xlabel('Relative Easting (m)')
    ax4.set_ylabel('Relative Northing (m)')
    ax4.grid(True)
    plot_timeseries(imu_data, imu_data['imu_stamps'])

    plt.tight_layout()
    plt.show()
    rclpy.shutdown()