## Virtual Environment
To prevent issues with running this code on other machines, the virtual environment `.venv` should be activated to make sure all necessary packages are available and versions are correct for how they are used in this lab.  

`setup.bash` will:

 create the `.venv` directory if it doesn't exist
 
 activate the venv
 
 source the ROS2 humble environment
 
 install all Python requirements 

 source the ROS2 packages in `src` with the build files created with `colcon build`


## Setup Instructions
after cloning and navigating to `/LAB4`: 
 in case I accidentally pushed my build folders:
 1. `rm -rf build install log`

 Then:

 2. `colcon build`

 3. **Usage options**:

 For just running the drivers:

 `source setup.bash`
 
 For running analysis:

 `source setup.bash analysis`


## Launch info for LAB4 driver
`fusion_driver` is a "launch" package that depends on `gps_driver`, `gps_message`, `imu_driver`, and `imu_msg`.

Run:

`ros2 launch fusion_driver fusion_launch.py gps_port:='<GPS port>' imu_port:='<IMU port>'`
