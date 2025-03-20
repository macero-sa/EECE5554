import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/savannah/EECE5554/LAB3/src/install/imu_driver'
