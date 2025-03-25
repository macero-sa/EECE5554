// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gps_message:msg/GpsMsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MESSAGE__MSG__DETAIL__GPS_MSG__STRUCT_H_
#define GPS_MESSAGE__MSG__DETAIL__GPS_MSG__STRUCT_H_

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
// Member 'utc_time'
// Member 'letter'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/GpsMsg in the package gps_message.
typedef struct gps_message__msg__GpsMsg
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String utc_time;
  double latitude;
  double longitude;
  double altitude;
  double utm_easting;
  double utm_northing;
  float hdop;
  int32_t zone;
  rosidl_runtime_c__String letter;
} gps_message__msg__GpsMsg;

// Struct for a sequence of gps_message__msg__GpsMsg.
typedef struct gps_message__msg__GpsMsg__Sequence
{
  gps_message__msg__GpsMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gps_message__msg__GpsMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GPS_MESSAGE__MSG__DETAIL__GPS_MSG__STRUCT_H_
