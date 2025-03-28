### Launch info
`fusion_driver` is a "launch" package that depends on `gps_driver`, `gps_message`, `imu_driver`, and `imu_msg`.

Run:

`ros2 launch fusion_driver fusion_launch.py gps_port:='<GPS port>' imu_port:='<IMU port>'`
