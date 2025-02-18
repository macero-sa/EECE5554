#!/usr/bin/env python3
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import struct
import numpy as np
from pyproj import Transformer

def parse_gps_message(data):
    """Parse binary GPS message data"""
    try:
        # Look for GPS1_Frame marker
        gps_marker_pos = data.find(b'GPS1_Frame')
        if gps_marker_pos == -1:
            return None
            
        # numeric data starts after "GPS1_Frame\0\0" (12 bytes)
        data_start = gps_marker_pos + 12
        
        # Verify we have enough data
        expected_length = data_start + 28  # 12 bytes header + 28 bytes data (lat, lon, alt, hdop)
        if len(data) < expected_length:
            print(f"Message too short: {len(data)} bytes")
            return None
            
        try:
            # Parse the basic fields
            values = {
                'latitude': struct.unpack('d', data[data_start:data_start + 8])[0],
                'longitude': struct.unpack('d', data[data_start + 8:data_start + 16])[0],
                'altitude': struct.unpack('d', data[data_start + 16:data_start + 24])[0],
                'hdop': struct.unpack('f', data[data_start + 24:data_start + 28])[0],
            }
            
            # Validate lat/lon
            if not (-90 <= values['latitude'] <= 90):
                # print(f"Invalid latitude: {values['latitude']}")
                return None
                
            if not (-180 <= values['longitude'] <= 180):
                # print(f"Invalid longitude: {values['longitude']}")
                return None
            
            # Calculate UTM coordinates from lat/lon
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:32619", always_xy=True)
            values['utm_easting'], values['utm_northing'] = transformer.transform(
                values['longitude'], values['latitude'])
            
            # Validate calculated UTM
            if values['utm_easting'] == 0 or values['utm_northing'] == 0:
                # print("Invalid calculated UTM coordinates (zero values)")
                return None
                
            if abs(values['utm_easting']) > 1e7 or abs(values['utm_northing']) > 1e7:
                # print(f"Suspicious UTM values: E={values['utm_easting']}, N={values['utm_northing']}")
                return None
                
            return values
                
        except struct.error as e:
            # print(f"Struct parsing error: {e}")
            return None
            
    except Exception as e:
        # print(f"Error parsing message: {e}")
        return None

def get_gps_data(db_path):
    """Get all GPS messages and parse them"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # First check what topics are available
    cursor.execute("SELECT id, name, type FROM topics")
    topics = cursor.fetchall()
    print("\nAvailable topics:")
    for topic_id, name, msg_type in topics:
        print(f"ID: {topic_id}, Name: {name}, Type: {msg_type}")
    
    # Then try to get messages
    cursor.execute("""
        SELECT m.timestamp, m.data
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        WHERE t.name = '/gps'
        ORDER BY m.timestamp
    """)
    
    timestamps = []
    coordinates = []
    
    print("\nProcessing messages...")
    total_messages = 0
    valid_messages = 0
    
    for i, (timestamp, data) in enumerate(cursor):
        total_messages += 1
        # if i < 3:  # Print first few raw messages for debugging
            # print(f"\nRaw message {i}:")
            # print(f"Timestamp: {timestamp}")
            # print(f"Data length: {len(data)} bytes")
            # print(f"Data starts with: {data[:20]}")  # Show first 20 bytes
            
        parsed = parse_gps_message(data)
        if parsed:
            valid_messages += 1
            timestamps.append(timestamp)
            coordinates.append(parsed)
            # print first few valid messages
            if valid_messages <= 3: 
                print(f"\nValid message {valid_messages}:")
                print(f"Lat: {parsed['latitude']:.6f}, Lon: {parsed['longitude']:.6f}")
                print(f"UTM E: {parsed['utm_easting']:.2f}, N: {parsed['utm_northing']:.2f}")
    
    print(f"\nProcessed {total_messages} total messages")
    print(f"Found {valid_messages} valid GPS messages")
    
    conn.close()
    return timestamps, coordinates

def get_topics(db_path):
    """Get list of topics in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, type FROM topics")
    topics = cursor.fetchall()
    conn.close()
    return topics

def get_messages_for_topic(db_path, topic_name):
    """Get messages for a specific topic"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.timestamp, m.data
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        WHERE t.name = ?
        ORDER BY m.timestamp
    """, (topic_name,))
    
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_table_info(db_path):
    """Get SQLite table structure"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\nDatabase tables:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
    
    conn.close()

def get_sample_message(db_path, topic_name, limit=1):
    """Get a sample message to examine its structure"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.timestamp, m.data, length(m.data) as data_length
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        WHERE t.name = ?
        LIMIT ?
    """, (topic_name, limit))
    
    messages = cursor.fetchall()
    conn.close()
    return messages

def plot_utm_path(df):
    """Plot the UTM path (easting vs northing)"""
    print("\nDetailed UTM Data Analysis:")
    print(f"Number of points: {len(df)}")
    print("\nFirst 5 raw UTM coordinates:")
    for i in range(min(5, len(df))):
        print(f"Point {i}: E={df['utm_easting'].iloc[i]}, N={df['utm_northing'].iloc[i]}")
    
    # Check for any invalid or zero values
    zero_utm = df[(df['utm_easting'] == 0) | (df['utm_northing'] == 0)]
    if not zero_utm.empty:
        print(f"\nFound {len(zero_utm)} points with zero coordinates")
    
    # Print range information
    print("\nUTM Ranges:")
    print(f"Easting: {df['utm_easting'].min():.2f} to {df['utm_easting'].max():.2f}")
    print(f"Northing: {df['utm_northing'].min():.2f} to {df['utm_northing'].max():.2f}")
    
    # Subtract first values to scale
    first_easting = df['utm_easting'].iloc[0]
    first_northing = df['utm_northing'].iloc[0]
    
    df['utm_easting_scaled'] = df['utm_easting'] - first_easting
    df['utm_northing_scaled'] = df['utm_northing'] - first_northing
    
    print("\nScaled UTM ranges (meters from start):")
    print(f"Easting: {df['utm_easting_scaled'].min():.2f} to {df['utm_easting_scaled'].max():.2f}")
    print(f"Northing: {df['utm_northing_scaled'].min():.2f} to {df['utm_northing_scaled'].max():.2f}")
    
    plt.figure(figsize=(10, 10))
    plt.scatter(df['utm_easting_scaled'], df['utm_northing_scaled'], 
               alpha=0.6, s=20, c='blue', marker='.')
    
    plt.plot(df['utm_easting_scaled'], df['utm_northing_scaled'], 
            'r-', alpha=0.5, linewidth=2.0)
    
    plt.xlabel('UTM Easting (m) - Relative to Start')
    plt.ylabel('UTM Northing (m) - Relative to Start')
    plt.title('UTM Coordinates (Relative to Starting Position)')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def plot_altitude_time(df, timestamps, description):
    """Plot altitude vs time"""
    # Print altitude statistics
    print("\nAltitude Statistics:")
    print("Range:", df['altitude'].min(), "to", df['altitude'].max())
    print("Mean:", df['altitude'].mean())
    
    # Convert timestamps to seconds from start
    start_time = timestamps[0]
    time_seconds = [(t - start_time) / 1e9 for t in timestamps]
    
    plt.figure(figsize=(12, 6))
    plt.plot(time_seconds, df['altitude'])
    plt.xlabel('Time (seconds)')
    plt.ylabel('Altitude (m)')
    plt.title(f'Altitude vs Time - {description}')
    plt.grid(True)
    plt.show()
    plt.close()

def plot_stationary_analysis(df, known_position=None):
    """Analyze stationary GPS data"""
    if known_position:
        # Convert known position from lat/lon to UTM
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32619", always_xy=True)
        known_utm_e, known_utm_n = transformer.transform(
            known_position[1],  # longitude
            known_position[0]   # latitude
        )
        
    # Use known position as reference point for scaling
    reference_e = known_utm_e
    reference_n = known_utm_n
    
    # Scale all points relative to the reference point
    df['utm_easting_scaled'] = df['utm_easting'] - reference_e
    df['utm_northing_scaled'] = df['utm_northing'] - reference_n
    
    if known_position:
        # Known position will be at (0,0) in scaled coordinates
        known_e_scaled = 0
        known_n_scaled = 0
    
    # Calculate Euclidean distances from known position
    df['error_distance'] = np.sqrt(df['utm_easting_scaled']**2 + df['utm_northing_scaled']**2)
    
    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Scatter plot
    ax1.scatter(df['utm_easting_scaled'], df['utm_northing_scaled'], 
               alpha=0.6, s=20, c='blue', marker='.', label='GPS Points')
    
    if known_position:
        ax1.scatter([known_e_scaled], [known_n_scaled], 
                   color='red', s=100, marker='*', label='Known Position')
    
    ax1.set_xlabel('UTM Easting (m) - Relative to Known Position')
    ax1.set_ylabel('UTM Northing (m) - Relative to Known Position')
    location_type = "Occluded" if known_position[0] == 42.33681 else "Open"
    ax1.set_title(f'Stationary GPS Track - {location_type} Location')
    ax1.grid(True)
    ax1.axis('equal')
    ax1.legend()
    
    # Plot 2: Histogram
    ax2.hist(df['error_distance'], bins=30, color='blue', alpha=0.7)
    ax2.set_xlabel('Error Distance (m)')
    ax2.set_ylabel('Frequency')
    ax2.set_title(f'Error Distribution - {location_type} Location')
    ax2.grid(True)
    
    # Add statistics to the plot
    stats_text = f'Mean Error: {df["error_distance"].mean():.2f}m\n'
    stats_text += f'Median Error: {df["error_distance"].median():.2f}m\n'
    stats_text += f'Std Dev: {df["error_distance"].std():.2f}m\n'
    stats_text += f'95th Percentile: {df["error_distance"].quantile(0.95):.2f}m'
    ax2.text(0.95, 0.95, stats_text,
             transform=ax2.transAxes,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    # Print statistics
    print("\nStationary Track Analysis:")
    print(f"Mean HDOP: {df['hdop'].mean():.2f}")

def plot_moving_analysis(df):
    """Analyze moving GPS data"""
    # Subtract first values to scale
    first_easting = df['utm_easting'].iloc[0]
    first_northing = df['utm_northing'].iloc[0]
    
    df['utm_easting_scaled'] = df['utm_easting'] - first_easting
    df['utm_northing_scaled'] = df['utm_northing'] - first_northing
    
    # Normalize the data before fitting to improve numerical stability
    x = df['utm_easting_scaled'].values
    y = df['utm_northing_scaled'].values
    
    # Center and scale the data
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_scaled = (x - x_mean) / np.std(x)
    y_scaled = (y - y_mean) / np.std(y)
    
    # Fit line to the normalized data
    coeffs = np.polyfit(x_scaled, y_scaled, 1)
    
    # Convert coefficients back to original scale
    slope = coeffs[0] * (np.std(y) / np.std(x))
    intercept = y_mean - slope * x_mean
    
    # Calculate line points for plotting
    x_range = np.linspace(df['utm_easting_scaled'].min(), df['utm_easting_scaled'].max(), 100)
    line_y = slope * x_range + intercept
    
    # Calculate perpendicular distance to line (error)
    df['line_error'] = np.abs(
        df['utm_northing_scaled'] - (slope * df['utm_easting_scaled'] + intercept)
    ) / np.sqrt(1 + slope**2)
    
    # Plot
    plt.figure(figsize=(10, 10))
    
    # Plot the GPS points
    plt.scatter(df['utm_easting_scaled'], df['utm_northing_scaled'], 
               alpha=0.6, s=20, c='blue', marker='.', label='GPS Points')
    
    # Plot the line of best fit
    plt.plot(x_range, line_y, 'r-', 
            alpha=1.0, linewidth=2.0, label=f'Best Fit Line (slope={slope:.3f})')
    
    plt.xlabel('UTM Easting (m) - Relative to Start')
    plt.ylabel('UTM Northing (m) - Relative to Start')
    plt.title('Walking with Best Fit Line')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()
    
    # Print statistics
    print("\nWalking Analysis:")
    print(f"Line slope: {slope:.3f}")
    print(f"Line intercept: {intercept:.3f}")
    print(f"RMS Error from line: {np.sqrt(np.mean(df['line_error']**2)):.2f} m")
    print(f"Mean HDOP: {df['hdop'].mean():.2f}")

def main():
    # kown position from google maps given in web mercator (lat, lon)
    known_position_occluded = (42.33681, -71.08740)  
    known_position_open = (42.33903, -71.08472)
    
    # dataset paths
    stationary_occluded = r"c:\RSN_local\lab1\occluded_spot.db3"
    stationary_open = r"c:\RSN_local\lab1\open_spot.db3"
    walking_file = r"c:\RSN_local\lab1\walking.db3"
    
    for file_path, description in [
        (stationary_occluded, "Stationary Occluded"),
        (stationary_open, "Stationary Open"),
        (walking_file, "Walking")
    ]:
        print(f"\nProcessing {description}...")
        timestamps, coordinates = get_gps_data(file_path)
        
        if coordinates:
            df = pd.DataFrame(coordinates)
            
            if "stationary" in description.lower():
                plot_stationary_analysis(df, known_position_occluded if "occluded" in description.lower() else known_position_open)
            else:
                plot_moving_analysis(df)
                
            plot_altitude_time(df, timestamps, description)
        else:
            print(f"No valid coordinates found in {description}")

if __name__ == "__main__":
    main()
