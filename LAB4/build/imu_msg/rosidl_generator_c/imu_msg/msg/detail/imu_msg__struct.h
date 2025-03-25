// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from imu_msg:msg/ImuMsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_H_
#define IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__struct.h"
// Member 'mag_field'
#include "sensor_msgs/msg/detail/magnetic_field__struct.h"
// Member 'raw_data'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ImuMsg in the package imu_msg.
typedef struct imu_msg__msg__ImuMsg
{
  std_msgs__msg__Header header;
  sensor_msgs__msg__Imu imu;
  sensor_msgs__msg__MagneticField mag_field;
  rosidl_runtime_c__String raw_data;
} imu_msg__msg__ImuMsg;

// Struct for a sequence of imu_msg__msg__ImuMsg.
typedef struct imu_msg__msg__ImuMsg__Sequence
{
  imu_msg__msg__ImuMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} imu_msg__msg__ImuMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_H_
