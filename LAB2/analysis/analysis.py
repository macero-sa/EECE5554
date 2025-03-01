import utm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def convert_to_decimal_degrees(nmea_value, direction):
    """Convert NMEA coordinate format (DDMM.MMMM) to decimal degrees"""
    if not nmea_value:
        return None
      
    try:
        degrees = float(nmea_value[:2])  # first 2 chars are degrees
        minutes = float(nmea_value[2:])  # decimal minutes
        decimal = degrees + minutes/60.0
        
        if direction in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    except (ValueError, IndexError):
        return None

def parse(line):
    if line.startswith('$GNGGA'):
        try:
            fields = line.strip().split(',')
            
            if len(fields) < 10:
                return None
                
            latitude = convert_to_decimal_degrees(fields[2], fields[3])
            if latitude is None:
                return None
                
            longitude = convert_to_decimal_degrees(fields[4], fields[5])
            if longitude is None:
                return None
                
            convert = utm.from_latlon(latitude, longitude)
            easting = convert[0]
            northing = convert[1]
            
            return easting, northing
                
        except (ValueError, IndexError):
            return None
    
    return None

def scatterplot(data, title):
    eastings = []
    northings = []
    valid_count = 0
    total_count = 0
    
    print(f"\nProcessing {title}:")
    print(f"Total lines in file: {len(data)}")
    
    for line in data:
        total_count += 1
        result = parse(line)
        if result:
            valid_count += 1
            eastings.append(result[0])
            northings.append(result[1])
    
    print(f"\nProcessed {total_count} total lines")
    print(f"Found {valid_count} valid GNGGA messages")
    
    if valid_count > 0:
        plt.figure(figsize=(10, 8))
        plt.scatter(eastings, northings, alpha=0.6)
        plt.title(f"{title} ({valid_count} points)")
        plt.xlabel('Easting (m)')
        plt.ylabel('Northing (m)')
        plt.grid(True)
        plt.axis('equal')
        
        # Fit line for the first and second quarters
        if valid_count > 1:
            quarter_index = valid_count // 4
            x1 = np.array(eastings[:quarter_index])
            y1 = np.array(northings[:quarter_index])
            x2 = np.array(eastings[quarter_index:2*quarter_index])
            y2 = np.array(northings[quarter_index:2*quarter_index])
            
            # Define the trimming percentages
            trim_front1 = 0.3  # 30% from the front of the first segment
            trim_end1 = 0.1     # 10% from the end of the first segment
            trim_front2 = 0.3  # 30% from the front of the second segment
            trim_end2 = 0.1     # 10% from the end of the second segment
            
            # Trim the first segment
            trim_count1_front = int(len(x1) * trim_front1)
            trim_count1_end = int(len(x1) * trim_end1)
            x1_trimmed = x1[trim_count1_front:len(x1) - trim_count1_end]
            y1_trimmed = y1[trim_count1_front:len(y1) - trim_count1_end]
            
            # Trim the second segment
            trim_count2_front = int(len(x2) * trim_front2)
            trim_count2_end = int(len(x2) * trim_end2)
            x2_trimmed = x2[trim_count2_front:len(x2) - trim_count2_end]
            y2_trimmed = y2[trim_count2_front:len(y2) - trim_count2_end]
            
            # Fit lines
            coeffs1 = np.polyfit(x1_trimmed, y1_trimmed, 1)
            coeffs2 = np.polyfit(x2_trimmed, y2_trimmed, 1)
            
            # Generate x values for the fitted lines
            x_fit1 = np.linspace(min(x1_trimmed), max(x1_trimmed), 100)
            y_fit1 = np.polyval(coeffs1, x_fit1)
            x_fit2 = np.linspace(min(x2_trimmed), max(x2_trimmed), 100)
            y_fit2 = np.polyval(coeffs2, x_fit2)
            
            # Plot fitted lines
            plt.plot(x_fit1, y_fit1, color='red', label='Line of Best Fit (Segment 1)')
            plt.plot(x_fit2, y_fit2, color='blue', label='Line of Best Fit (Segment 2)')
            plt.legend()
            
            # Calculate RMS error for both segments
            y_pred1 = np.polyval(coeffs1, x1_trimmed)
            y_pred2 = np.polyval(coeffs2, x2_trimmed)
            rms_error1 = np.sqrt(np.mean((y1_trimmed - y_pred1) ** 2))
            rms_error2 = np.sqrt(np.mean((y2_trimmed - y_pred2) ** 2))
            
            print(f"RMS Error for Segment 1: {rms_error1:.3f} m")
            print(f"RMS Error for Segment 2: {rms_error2:.3f} m")
        
        plt.show()
    else:
        print("No valid points to plot!")
    
def plot_stationary_stats(data, title):
    eastings = []
    northings = []
    
    for line in data:
        result = parse(line)
        if result:
            eastings.append(result[0])
            northings.append(result[1])
    
    if len(eastings) > 0:
        # mean positions
        mean_easting = np.mean(eastings)
        mean_northing = np.mean(northings)
        
        # euclidean distances from mean position
        distances = np.sqrt(
            (np.array(eastings) - mean_easting)**2 + 
            (np.array(northings) - mean_northing)**2
        )
        
        # histogram
        plt.figure(figsize=(10, 6))
        plt.hist(distances, bins=30, alpha=0.75)
        plt.title(f'Distance from Mean Position - {title}')
        plt.xlabel('Distance (m)')
        plt.ylabel('Frequency')
        
        # statistics
        mean_distance = np.mean(distances)
        std_dev_distance = np.std(distances)
        max_distance = np.max(distances)
        
        stats_text = f'Mean Distance: {mean_distance:.3f}m\n'
        stats_text += f'Std Dev Distance: {std_dev_distance:.3f}m\n'
        stats_text += f'Max Distance: {max_distance:.3f}m'
        
        plt.text(0.95, 0.95, stats_text,
                transform=plt.gca().transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.grid(True)
        plt.show()
    else:
        print(f"No valid points for {title}")

def main():
    files = [
        ('data/openwalk.txt', 'Open Walking'),
        ('data/walk_occluded_1.txt', 'Occluded Walking')
        # ('data/stationary_occluded_2.txt', 'Stationary Occluded'),
        # ('data/open_stat.txt', 'Open Stationary dev1'),
        # ('data/stationary_open_0.txt', 'Open Stationary dev2'),
        # ('data_1/open_stationary.txt', 'Lanzi Open Stationary')
        # ('data_1/open_rect.txt', 'Lanzi Open Rect')
    ]
    
    for file_path, title in files:
        try:
            with open(file_path, 'rb') as f:
                data = [line.decode('utf-8', errors='ignore') for line in f.readlines()]
            
            scatterplot(data, title)
            
            if 'stationary' in title.lower():
                plot_stationary_stats(data, title)
                
        except FileNotFoundError:
            print(f"Error: Could not find file {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()