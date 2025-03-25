// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gps_message:msg/GpsMsg.idl
// generated code does not contain a copyright notice

#ifndef GPS_MESSAGE__MSG__DETAIL__GPS_MSG__BUILDER_HPP_
#define GPS_MESSAGE__MSG__DETAIL__GPS_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gps_message/msg/detail/gps_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gps_message
{

namespace msg
{

namespace builder
{

class Init_GpsMsg_letter
{
public:
  explicit Init_GpsMsg_letter(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  ::gps_message::msg::GpsMsg letter(::gps_message::msg::GpsMsg::_letter_type arg)
  {
    msg_.letter = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_zone
{
public:
  explicit Init_GpsMsg_zone(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_letter zone(::gps_message::msg::GpsMsg::_zone_type arg)
  {
    msg_.zone = std::move(arg);
    return Init_GpsMsg_letter(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_hdop
{
public:
  explicit Init_GpsMsg_hdop(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_zone hdop(::gps_message::msg::GpsMsg::_hdop_type arg)
  {
    msg_.hdop = std::move(arg);
    return Init_GpsMsg_zone(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_utm_northing
{
public:
  explicit Init_GpsMsg_utm_northing(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_hdop utm_northing(::gps_message::msg::GpsMsg::_utm_northing_type arg)
  {
    msg_.utm_northing = std::move(arg);
    return Init_GpsMsg_hdop(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_utm_easting
{
public:
  explicit Init_GpsMsg_utm_easting(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_utm_northing utm_easting(::gps_message::msg::GpsMsg::_utm_easting_type arg)
  {
    msg_.utm_easting = std::move(arg);
    return Init_GpsMsg_utm_northing(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_altitude
{
public:
  explicit Init_GpsMsg_altitude(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_utm_easting altitude(::gps_message::msg::GpsMsg::_altitude_type arg)
  {
    msg_.altitude = std::move(arg);
    return Init_GpsMsg_utm_easting(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_longitude
{
public:
  explicit Init_GpsMsg_longitude(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_altitude longitude(::gps_message::msg::GpsMsg::_longitude_type arg)
  {
    msg_.longitude = std::move(arg);
    return Init_GpsMsg_altitude(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_latitude
{
public:
  explicit Init_GpsMsg_latitude(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_longitude latitude(::gps_message::msg::GpsMsg::_latitude_type arg)
  {
    msg_.latitude = std::move(arg);
    return Init_GpsMsg_longitude(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_utc_time
{
public:
  explicit Init_GpsMsg_utc_time(::gps_message::msg::GpsMsg & msg)
  : msg_(msg)
  {}
  Init_GpsMsg_latitude utc_time(::gps_message::msg::GpsMsg::_utc_time_type arg)
  {
    msg_.utc_time = std::move(arg);
    return Init_GpsMsg_latitude(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

class Init_GpsMsg_header
{
public:
  Init_GpsMsg_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GpsMsg_utc_time header(::gps_message::msg::GpsMsg::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_GpsMsg_utc_time(msg_);
  }

private:
  ::gps_message::msg::GpsMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::gps_message::msg::GpsMsg>()
{
  return gps_message::msg::builder::Init_GpsMsg_header();
}

}  // namespace gps_message

#endif  // GPS_MESSAGE__MSG__DETAIL__GPS_MSG__BUILDER_HPP_
