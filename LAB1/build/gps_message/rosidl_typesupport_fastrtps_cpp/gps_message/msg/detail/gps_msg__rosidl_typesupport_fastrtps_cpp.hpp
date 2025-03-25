// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from gps_message:msg/GpsMsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MESSAGE__MSG__DETAIL__GPS_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define GPS_MESSAGE__MSG__DETAIL__GPS_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "gps_message/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "gps_message/msg/detail/gps_msg__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace gps_message
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gps_message
cdr_serialize(
  const gps_message::msg::GpsMsg & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gps_message
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  gps_message::msg::GpsMsg & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gps_message
get_serialized_size(
  const gps_message::msg::GpsMsg & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gps_message
max_serialized_size_GpsMsg(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace gps_message

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gps_message
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, gps_message, msg, GpsMsg)();

#ifdef __cplusplus
}
#endif

#endif  // GPS_MESSAGE__MSG__DETAIL__GPS_MSG__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
