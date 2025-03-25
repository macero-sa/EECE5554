// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from gps_message:msg/GpsMsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MESSAGE__MSG__DETAIL__GPS_MSG__TRAITS_HPP_
#define GPS_MESSAGE__MSG__DETAIL__GPS_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "gps_message/msg/detail/gps_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace gps_message
{

namespace msg
{

inline void to_flow_style_yaml(
  const GpsMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: utc_time
  {
    out << "utc_time: ";
    rosidl_generator_traits::value_to_yaml(msg.utc_time, out);
    out << ", ";
  }

  // member: latitude
  {
    out << "latitude: ";
    rosidl_generator_traits::value_to_yaml(msg.latitude, out);
    out << ", ";
  }

  // member: longitude
  {
    out << "longitude: ";
    rosidl_generator_traits::value_to_yaml(msg.longitude, out);
    out << ", ";
  }

  // member: altitude
  {
    out << "altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude, out);
    out << ", ";
  }

  // member: utm_easting
  {
    out << "utm_easting: ";
    rosidl_generator_traits::value_to_yaml(msg.utm_easting, out);
    out << ", ";
  }

  // member: utm_northing
  {
    out << "utm_northing: ";
    rosidl_generator_traits::value_to_yaml(msg.utm_northing, out);
    out << ", ";
  }

  // member: hdop
  {
    out << "hdop: ";
    rosidl_generator_traits::value_to_yaml(msg.hdop, out);
    out << ", ";
  }

  // member: zone
  {
    out << "zone: ";
    rosidl_generator_traits::value_to_yaml(msg.zone, out);
    out << ", ";
  }

  // member: letter
  {
    out << "letter: ";
    rosidl_generator_traits::value_to_yaml(msg.letter, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GpsMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: utc_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "utc_time: ";
    rosidl_generator_traits::value_to_yaml(msg.utc_time, out);
    out << "\n";
  }

  // member: latitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "latitude: ";
    rosidl_generator_traits::value_to_yaml(msg.latitude, out);
    out << "\n";
  }

  // member: longitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "longitude: ";
    rosidl_generator_traits::value_to_yaml(msg.longitude, out);
    out << "\n";
  }

  // member: altitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "altitude: ";
    rosidl_generator_traits::value_to_yaml(msg.altitude, out);
    out << "\n";
  }

  // member: utm_easting
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "utm_easting: ";
    rosidl_generator_traits::value_to_yaml(msg.utm_easting, out);
    out << "\n";
  }

  // member: utm_northing
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "utm_northing: ";
    rosidl_generator_traits::value_to_yaml(msg.utm_northing, out);
    out << "\n";
  }

  // member: hdop
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hdop: ";
    rosidl_generator_traits::value_to_yaml(msg.hdop, out);
    out << "\n";
  }

  // member: zone
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "zone: ";
    rosidl_generator_traits::value_to_yaml(msg.zone, out);
    out << "\n";
  }

  // member: letter
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "letter: ";
    rosidl_generator_traits::value_to_yaml(msg.letter, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GpsMsg & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace gps_message

namespace rosidl_generator_traits
{

[[deprecated("use gps_message::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gps_message::msg::GpsMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  gps_message::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gps_message::msg::to_yaml() instead")]]
inline std::string to_yaml(const gps_message::msg::GpsMsg & msg)
{
  return gps_message::msg::to_yaml(msg);
}

template<>
inline const char * data_type<gps_message::msg::GpsMsg>()
{
  return "gps_message::msg::GpsMsg";
}

template<>
inline const char * name<gps_message::msg::GpsMsg>()
{
  return "gps_message/msg/GpsMsg";
}

template<>
struct has_fixed_size<gps_message::msg::GpsMsg>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gps_message::msg::GpsMsg>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gps_message::msg::GpsMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // GPS_MESSAGE__MSG__DETAIL__GPS_MSG__TRAITS_HPP_
