import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from datetime import datetime, timezone
import serial
from gps_message.msg import GpsMsg
from pyproj import Proj
# from rclpy.time import Time
# from rclpy.duration import Duration

class Driver(Node):
    def __init__(self):
        super().__init__('gps_driver')
        # create object attributes: publisher, serial port, timer, and counter  
        self.publisher = self.create_publisher(GpsMsg, '/gps', 10)
        self.declare_parameter('port', '/dev/pts/16')
        self.serial_port = self.get_parameter('port').value
        
        try:
            self.ser = serial.Serial(self.serial_port, 4800)
            self.get_logger().info(f'Successfully connected to port {self.serial_port}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to open port {self.serial_port}: {e}')
            raise
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)


    
    def timer_callback(self):
        try:
            line = self.ser.readline().decode('utf-8')
            if line.startswith('$GPGGA'):  # Only log GPGGA messages
                parsed_data = self.parse_str(line)
                if parsed_data:
                    lat, lon, hdop, alt, header, utc_time = parsed_data
                    
                    t, nt = utc_time.split('.')
                    dt = datetime.strptime(t, "%H%M%S")
                    sec = dt.hour * 3600 + dt.minute * 60 + dt.second
                    nsec = int(float('0.' + nt) * 1e9)  # Convert decimal part to nanoseconds

                    zone, letter = self.zone_letter(lat, lon)
                    utm_easting, utm_northing = self.latlon_to_utm(lat, lon, zone)
                    gps_message = GpsMsg()
                    gps_message.header = Header()
                    gps_message.header.stamp.sec = sec
                    gps_message.header.stamp.nanosec = nsec
                    gps_message.header.frame_id = 'GPS1_Frame'
                    gps_message.latitude = lat
                    gps_message.longitude = lon
                    gps_message.hdop = hdop
                    gps_message.altitude = alt
                    gps_message.utm_easting = utm_easting
                    gps_message.utm_northing = utm_northing
                    gps_message.zone = zone
                    gps_message.letter = letter
                    gps_message.utc_time = utc_time
                    self.publisher.publish(gps_message)
                    self.get_logger().info(f'Publishing: {gps_message}')

                else:
                    self.get_logger().warn('No data received from GPS')
        except Exception as e:
            self.get_logger().error(f'Error reading from serial port: {e}')
            


    def parse_str(self, line):
        if line.startswith('$GPGGA'):
            fields = line.strip().split(',')
            # raw field index: log header 0, utc time 1, lat 2, lat dir3, lon 4, lon dir 5, hdop8, alt9
            raw_header = fields[0]
            utc_time = fields[1]  # Keep as string for time calculations
            raw_lat = fields[2]
            lat_dir = fields[3]
            raw_lon = fields[4]
            lon_dir = fields[5]
            hdop = float(fields[8])
            alt = float(fields[9]) 
            
            lat = self.signed_decimal(raw_lat, lat_dir)
            lon = self.signed_decimal(raw_lon, lon_dir)
            header = raw_header.strip('$')
            return lat, lon, hdop, alt, header, utc_time
        else:
            return None
    
    def signed_decimal(self, val, direction):
        # first convert from deg/min/s to decimal
        # degrees are first 2 digits if latitude (N or S), else first 3 digits
        if direction in ['N', 'S']:
            degrees = int(val[:2])
            minutes = float(val[2:])
        else:
            degrees = int(val[:3])
            minutes = float(val[3:])
        decimal_val = degrees + (minutes / 60)
        # val is negative if direction is S or W
        if direction in ['S', 'W',]:
            decimal_val *= -1
        return decimal_val


    def zone_letter(self, lat, lon):
        # utm zone conversion 
        zone = int((lon + 180) / 6) + 1
        # letters only assigned if lat is between 80deg S or 84deg N, indexed every 8deg. 
        lat_band_letters = "CDEFGHJKLMNPQRSTUVWX"
        ''' lat_band_ranges = range(-80, 85, 8)'''
    
        # X = letter_n-1 spans 12 deg instead of 8
        if lat < -80 or lat > 84:
            letter = None  
        else:
            index = (lat - (-80)) // 8
            letter = lat_band_letters[int(index)]

        return zone, letter    

    
    def latlon_to_utm(self, lat, lon, zone):
        # get utm projection
        proj_utm = Proj(proj='utm', zone=zone, ellps='WGS84', south=(lat < 0))
        # transform lat/lon to UTM
        utm_easting, utm_northing = proj_utm(lon, lat)
        return utm_easting, utm_northing
    
def main(args=None):
    rclpy.init(args=args)
    gps_driver = Driver()
    rclpy.spin(gps_driver)
    gps_driver.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()