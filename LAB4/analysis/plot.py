import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyproj import Transformer
import rosbag2_py
from scipy.spatial.transform import Rotation as R
import numpy as np
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
                
            # if imu_count % 1000 == 0 or gps_count % 50 == 0:
            #     print(f"Processed {imu_count} IMU messages and {gps_count} GPS messages")
                
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



def main(): 
    # dataset paths

    data_driving = '/home/savannah/EECE5554/LAB4/data/data_driving/data_driving_0.db3'
    data_circles = '/home/savannah/EECE5554/LAB4/data/data_going_in_circles/data_going_in_circles_0.db3'
    data_emulator = '/home/savannah/EECE5554/LAB4/data/test_no_alt_dfl/test_no_alt_dfl_0.db3'
    data_newton = '/home/savannah/EECE5554/LAB4/data/data_driving2/data_driving2_0.db3'
    data_commute = '/home/savannah/EECE5554/LAB4/data/data_commute2/data_commute2_0.db3'
    
    for file_path, description in [
        # (data_driving, "Driving on Campus"),
        # (data_circles, "Circles on Campus"),
        (data_emulator, "Emulator Test"),
        (data_newton, "Driving in Newton"),
        (data_commute, "Driving Commute")
    ]:
        print(f"\nProcessing {description}...")
        imu_data, gps_data = read_data(file_path)

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
        # plot_timeseries(imu_data, imu_data['imu_stamps'])

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()