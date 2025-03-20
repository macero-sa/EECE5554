// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from imu_msg:msg/ImuMsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSG__MSG__DETAIL__IMU_MSG__BUILDER_HPP_
#define IMU_MSG__MSG__DETAIL__IMU_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "imu_msg/msg/detail/imu_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace imu_msg
{

namespace msg
{

namespace builder
{

class Init_ImuMsg_raw_data
{
public:
  explicit Init_ImuMsg_raw_data(::imu_msg::msg::ImuMsg & msg)
  : msg_(msg)
  {}
  ::imu_msg::msg::ImuMsg raw_data(::imu_msg::msg::ImuMsg::_raw_data_type arg)
  {
    msg_.raw_data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::imu_msg::msg::ImuMsg msg_;
};

class Init_ImuMsg_mag_field
{
public:
  explicit Init_ImuMsg_mag_field(::imu_msg::msg::ImuMsg & msg)
  : msg_(msg)
  {}
  Init_ImuMsg_raw_data mag_field(::imu_msg::msg::ImuMsg::_mag_field_type arg)
  {
    msg_.mag_field = std::move(arg);
    return Init_ImuMsg_raw_data(msg_);
  }

private:
  ::imu_msg::msg::ImuMsg msg_;
};

class Init_ImuMsg_imu
{
public:
  explicit Init_ImuMsg_imu(::imu_msg::msg::ImuMsg & msg)
  : msg_(msg)
  {}
  Init_ImuMsg_mag_field imu(::imu_msg::msg::ImuMsg::_imu_type arg)
  {
    msg_.imu = std::move(arg);
    return Init_ImuMsg_mag_field(msg_);
  }

private:
  ::imu_msg::msg::ImuMsg msg_;
};

class Init_ImuMsg_header
{
public:
  Init_ImuMsg_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ImuMsg_imu header(::imu_msg::msg::ImuMsg::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ImuMsg_imu(msg_);
  }

private:
  ::imu_msg::msg::ImuMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::imu_msg::msg::ImuMsg>()
{
  return imu_msg::msg::builder::Init_ImuMsg_header();
}

}  // namespace imu_msg

#endif  // IMU_MSG__MSG__DETAIL__IMU_MSG__BUILDER_HPP_
