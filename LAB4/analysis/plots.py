import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyproj import Transformer
from scipy.integrate import cumulative_trapezoid
import rosbag2_py
from scipy.spatial.transform import Rotation as R
import numpy as np
import rclpy.serialization
import rosbag2_py
from imu_msg.msg import ImuMsg
from gps_message.msg import GpsMsg
import rclpy
from scipy.signal import butter, filtfilt
from scipy import signal
from scipy.interpolate import interp1d

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
def circles():
# dataset paths
    data_driving = '/home/savannah/EECE5554/LAB4/rdata/data_driving/data_driving_0.db3'
    data_circles = '/home/savannah/EECE5554/LAB4/rdata/data_going_in_circles/data_going_in_circles_0.db3'
    file_path, description = [(data_circles, "Circles"), (data_driving, "Driving")]
    imu_data, gps_data = read_data(data_circles)    
    time = imu_data['imu_stamps']
    time = time - time[0]  
    time_seconds = (time) * 1e-9              
    mag_data = imu_data['mag']
    mag_x = mag_data[:, 0]
    mag_y = mag_data[:, 1]
    mag_z = mag_data[:, 2]
    # save unprocessed data
    mag_xraw = mag_x
    mag_yraw = mag_y
    mag_zraw = mag_z
    # trim front and back
    mag_x = mag_x[800:2300]
    mag_y = mag_y[800:2300]
    mag_z = mag_z[800:2300]
    time = time[800:2300]

    # find center
    center_x = (np.max(mag_x) + np.min(mag_x)) / 2
    center_y = (np.max(mag_y) + np.min(mag_y)) / 2
    print(f"Center: ({center_x}, {center_y})")
    mag_xhi = mag_x - center_x
    mag_yhi = mag_y - center_y

    data = np.column_stack((mag_xhi, mag_yhi))
    covariance_matrix = np.cov(data.T)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    # get scaling
    scale_factors = np.sqrt(eigenvalues)
    max_scale = np.max(scale_factors)
    scaling_matrix = np.diag(max_scale / scale_factors)
    # Create circularization matrix
    S = eigenvectors @ scaling_matrix @ eigenvectors.T
    mag_cal = (S @ data.T).T
    mag_xsi = mag_cal[:, 0]
    mag_ysi = mag_cal[:, 1]

    # plt.figure(figsize=(15, 5))
    # plt.subplot(1, 3, 1)
    # plt.plot(mag_x, mag_y)
    # plt.plot(0, 0, 'ro', label='Desired Center')
    # plt.title('Trimmed Uncorrected')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.axis('equal')
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(1, 3, 2)
    # plt.plot(mag_xhi, mag_yhi)
    # plt.plot(0, 0, 'ro', label='Desired Center')
    # plt.title('Hard Iron Corrected')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.axis('equal')
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(1, 3, 3)
    # plt.plot(mag_xsi, mag_ysi)
    # plt.title('Hard & Soft Corrected')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.axis('equal')
    # plt.grid(True)
    # plt.tight_layout()

    # plt.show()

    # get yaw angle from mag x mag y
    yaw = np.degrees(np.arctan2(mag_y, mag_x))
    yaw_cal = np.degrees(np.arctan2(mag_ysi, mag_xsi))
    # plt.figure
    # plt.plot(time,yaw, label='Yaw')
    # plt.plot(time,yaw_cal, label='Yaw Calibrated')
    # plt.title('Circles: Yaw Angle')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Yaw (degrees)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    # axs[0].scatter(time, mag_x, s=1,label='Raw')
    # axs[0].scatter(time, mag_xsi, s=1,label='Corrected')
    # axs[0].set_xlabel('Seconds')
    # axs[0].set_ylabel('Tesla')
    # axs[0].set_title('Circles: Mag X vs Time')
    # axs[0].legend()
    # axs[0].grid(True)
    # axs[1].scatter(time, mag_y, s=1,label='Raw')
    # axs[1].scatter(time, mag_ysi,s=1,label='Corrected')
    # axs[1].set_xlabel('Seconds')
    # axs[1].set_ylabel('Tesla')
    # axs[1].set_title('Circles: Mag Y vs Time')
    # axs[1].legend()
    # axs[1].grid(True)
    # plt.tight_layout()

    # plt.show()
    # plt.show()

    return S, center_x, center_y



    main()
def driving():
    S, center_x, center_y = circles()
    data_driving = '/home/savannah/EECE5554/LAB4/rdata/data_driving/data_driving_0.db3'
    imu_data, gps_data = read_data(data_driving)
    # use S to correct driving data
    time = imu_data['imu_stamps']   
    time = time - time[0]      
    time_seconds = (time) * 1e-9            
    mag_data = imu_data['mag']
    mag_x = mag_data[:, 0]
    mag_y = mag_data[:, 1]
    mag_z = mag_data[:, 2]
    mag_xhi = mag_x - center_x
    mag_yhi = mag_y - center_y
    data = np.column_stack((mag_xhi, mag_yhi))
    mag_cal = (S @ data.T).T

    yawMag = np.degrees(np.arctan2(mag_cal[:,1], mag_cal[:,0]))
    yaw_calMag = np.degrees(np.arctan2(mag_cal[:,1], mag_cal[:,0]))

    # plt.figure
    # plt.plot(time_seconds,yawMag,linewidth=2, label='Yaw')
    # plt.plot(time_seconds,yaw_calMag, linewidth=0.75,label='Yaw Calibrated')
    # plt.title('Driving: Raw vs Corrected Yaw (Mag)')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Yaw (degrees)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    # axs[0].scatter(time_seconds, mag_x, s=1,label='Raw')
    # axs[0].scatter(time_seconds, mag_cal[:,0], s=1,label='Corrected')
    # axs[0].set_xlabel('Seconds')
    # axs[0].set_ylabel('Tesla')
    # axs[0].set_title('Driving: Mag X vs Time')
    # axs[0].legend()
    # axs[0].grid(True)
    # axs[1].scatter(time_seconds, mag_y, s=1,label='Raw')
    # axs[1].scatter(time_seconds, mag_cal[:,1],s=1,label='Corrected')
    # axs[1].set_xlabel('Seconds')
    # axs[1].set_ylabel('Tesla')
    # axs[1].set_title('Driving: Mag Y vs Time')
    # axs[1].legend()
    # axs[1].grid(True)
    # plt.tight_layout()
    # plt.show()
    
    # integrate angular velocity to get yaw anlge
    gyro_data = imu_data['gyro']
    gyro_x = gyro_data[:, 0]
    gyro_y = gyro_data[:, 1]
    gyro_z = gyro_data[:, 2]
    yaw_int = cumulative_trapezoid(gyro_z, time_seconds, initial=0)
    yaw_int =np.rad2deg(yaw_int.astype(np.float64))
    yaw_int = yaw_int + yaw_calMag[0]
    yaw_int = -1 *((yaw_int + 180) % 360 - 180)

    # plt.figure
    # plt.plot(time_seconds,yaw_int, '--', linewidth=2,label='Yaw from Gyro')
    # plt.plot(time_seconds,yaw_calMag, '-', linewidth=1,label='Yaw Mag Calibrated')
    # plt.title('Yaw: Integrated vs Measured')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Yaw (degrees)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    ## filtering
    order = 2
    fs = 40 # Hz
    nyquist = 0.5 * fs
    def butterworth(data,cutoff,type):
        normal_cutoff = cutoff / nyquist
        sos = signal.butter(order, normal_cutoff, btype=type, analog=False, output='sos')
        y = signal.sosfilt(sos, data)
        return y
    
    yaw_measured = butterworth(yaw_calMag,0.08, 'low')
    yaw_integrated = butterworth(yaw_int,0.0001, 'high')

    alpha = 0.7
    yaw_fusion = alpha * yaw_measured + (1 - alpha) * yaw_integrated

    # plot yaw from euler angle
    q = imu_data['orient']
    euler = quat_to_euler(q)
    yaw_euler = -euler[:, 2]
    print(f"Yaw Euler size: {yaw_euler.shape}")

    # plt.figure
    # plt.plot(time_seconds,yaw_integrated, '-', linewidth=1,label='Estimated Yaw')
    # plt.plot(time_seconds,yaw_measured, '-', linewidth=1,label='Measured Yaw(Mag)')
    # plt.plot(time_seconds,yaw_euler, '-', linewidth=1,label='Measured Yaw (Euler)')
    # plt.plot(time_seconds,yaw_fusion, '-', linewidth=1,label='Informed Estimated Yaw (fusion)')

    # plt.title('Filtered Yaw Comparisons')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Yaw (degrees)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    #GPS Velocity
    time_gps = gps_data['gps_stamps']    
    time_gps = time_gps - time_gps[0]
    timegps_seconds = (time_gps) * 1e-9
    northing = gps_data['northing']
    easting = gps_data['easting']
    dt = np.diff(timegps_seconds)
    d_northing = np.diff(northing)
    d_easting = np.diff(easting)
    
    # Compute distance and velocity
    dists = np.sqrt(d_northing**2 + d_easting**2)
    velocity_gps = dists / dt
    # Interpolate to match IMU timestamps
    max_realistic_speed = 30  # m/s (~108 km/h)
    velocity_gps[velocity_gps > max_realistic_speed] = max_realistic_speed
    
    # Create timestamps for velocities (midpoints between GPS readings)
    time_vel_gps = timegps_seconds[:-1] + dt/2
    vel_interp = interp1d(time_vel_gps, velocity_gps, 
                         kind='linear', 
                         fill_value='extrapolate')
    print(f"IMU timestamps: {len(time_seconds)}")
    velocity_gps_interp = vel_interp(time_seconds)   
    print(f"GPS velocity range: {np.min(velocity_gps):.2f} to {np.max(velocity_gps):.2f} m/s")
    # Integrate lin accel to estimate forward velocity
    ax = imu_data['accel'][:, 0]
    ay = imu_data['accel'][:, 1]
    az = imu_data['accel'][:, 2]
    n_static = 100  # Number of initial static samples
    ax_bias = np.mean(ax[:n_static])
    ay_bias = np.mean(ay[:n_static])
    az_bias = np.mean(az[:n_static])
    
    # Remove gravity using orientation
    q = imu_data['orient']
    r = R.from_quat(q)
    gravity = np.array([0, 0, 9.81]) 
    acc_world = []
    for i in range(len(ax)):
        acc_body = np.array([ax[i] - ax_bias, 
                           ay[i] - ay_bias, 
                           az[i] - az_bias])
        # Transform to world frame
        acc_w = r[i].apply(acc_body)
        # Remove gravity
        acc_w[2] -= 9.81
        acc_world.append(acc_w)
    
    acc_corrected = np.array(acc_world)  
    acc_corrected = np.array(acc_corrected)
    
    static_threshold = np.percentile(velocity_gps_interp, 15)  # Bottom 10% of speeds
    print(f"Suggested velocity threshold from GPS: {static_threshold:.3f} m/s")
    
    # Apply zero-velocity update when vehicle is stationary
    velocity_threshold = 0.1 
    acc_magnitude = np.sqrt(np.sum(acc_corrected**2, axis=1))
    static_mask = acc_magnitude < velocity_threshold
    acc_corrected[static_mask] = 0

    vx = cumulative_trapezoid(acc_corrected[:, 0], time_seconds, initial=0)
    vy = cumulative_trapezoid(acc_corrected[:, 1], time_seconds, initial=0)
    vxfilt = butterworth(vx, 0.005, 'high')  
    vyfilt = butterworth(vy, 0.005, 'high')
    
    speed_imu = np.sqrt(vx**2 + vy**2)
    speed_imu_filt = np.sqrt(vxfilt**2 + vyfilt**2)
    max_gps_speed = np.max(velocity_gps_interp)
    max_imu_speed = np.max(speed_imu_filt)
    scale_factor = max_gps_speed / max_imu_speed
    speed_imu_filt = speed_imu_filt * scale_factor
    print(f'scale factor: {scale_factor:.2f}')
    
    # Plot velocity comparisons
    # plt.figure(figsize=(12, 8))
    # plt.plot(time_seconds, speed_imu, '--', linewidth=1, label='IMU Raw', alpha=0.5)
    # plt.plot(time_seconds, speed_imu_filt, '-', linewidth=2, label='IMU Corrected') 
    # plt.title('Vehicle Speed Estimates')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Speed (m/s)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12, 8))
    # plt.plot(time_seconds, speed_imu_filt, '-', linewidth=2, label='IMU Corrected')
    # plt.plot(time_seconds, velocity_gps_interp, '-', linewidth=1, label='GPS') 
    # plt.title('Vehicle Speed Estimates')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Speed (m/s)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

    # Dead Reckoning

    wXdot = gyro_z * speed_imu_filt
    # integrate
    yaw_deg = np.deg2rad(yaw_fusion)
    northing_rel = northing - northing[0]
    easting_rel = easting - easting[0]
    
    # Get initial heading from GPS
    gps_heading = np.arctan2(np.diff(northing_rel[:2]), np.diff(easting_rel[:2]))
    imu_heading = np.deg2rad(yaw_fusion[0])
    heading_correction = gps_heading - imu_heading

    vn = speed_imu_filt * np.sin(yaw_deg + heading_correction)
    ve = speed_imu_filt * np.cos(yaw_deg + heading_correction)

    # Get position from velocity
    xn = cumulative_trapezoid(vn, time_seconds, initial=0)
    xe = cumulative_trapezoid(ve, time_seconds, initial=0)

    theta = (7 * np.pi) / 12  # 90 degrees in radians
    rot = np.array([[np.cos(theta), -np.sin(theta)],
                              [np.sin(theta), np.cos(theta)]])
    
    xe_rotated, xn_rotated = rot @ np.vstack((xe, xn))

    Xdot = cumulative_trapezoid(wXdot, time_seconds, initial=0)
    difference = wXdot - Xdot
    print(f"Max difference: {np.max(difference):.2f} m/s")
    # plt.figure(figsize=(12, 8))
    # plt.plot(time_seconds, wXdot, '-', linewidth=2, label='wXdot')
    # plt.plot(time_seconds, Xdot, '-', linewidth=1, label='Xdot') 
    # plt.title('Dead reackoning')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Speed (m/s)')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

    # plt.figure(figsize=(12, 10))
    # plt.scatter(easting_rel, northing_rel, c='blue', label='GPS', alpha=0.5)
    # plt.scatter(xe_rotated, xn_rotated, c='red', label='Dead Reckoning', alpha=0.25)
    # plt.title('Relative Position Trajectories')
    # plt.xlabel('Relative Easting (m)')
    # plt.ylabel('Relative Northing (m)')
    # plt.grid(True)
    # plt.legend()
    # plt.axis('equal')  # Equal scaling for both axes
    # plt.tight_layout()
    # plt.show()


if __name__ == "__main__":
    # circles()
    driving()
