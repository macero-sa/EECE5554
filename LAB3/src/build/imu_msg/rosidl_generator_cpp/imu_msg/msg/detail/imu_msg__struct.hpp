// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from imu_msg:msg/ImuMsg.idl
// generated code does not contain a copyright notice

#ifndef IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_HPP_
#define IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'imu'
#include "sensor_msgs/msg/detail/imu__struct.hpp"
// Member 'mag_field'
#include "sensor_msgs/msg/detail/magnetic_field__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__imu_msg__msg__ImuMsg __attribute__((deprecated))
#else
# define DEPRECATED__imu_msg__msg__ImuMsg __declspec(deprecated)
#endif

namespace imu_msg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ImuMsg_
{
  using Type = ImuMsg_<ContainerAllocator>;

  explicit ImuMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    imu(_init),
    mag_field(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->raw_data = "";
    }
  }

  explicit ImuMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    imu(_alloc, _init),
    mag_field(_alloc, _init),
    raw_data(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->raw_data = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _imu_type =
    sensor_msgs::msg::Imu_<ContainerAllocator>;
  _imu_type imu;
  using _mag_field_type =
    sensor_msgs::msg::MagneticField_<ContainerAllocator>;
  _mag_field_type mag_field;
  using _raw_data_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _raw_data_type raw_data;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__imu(
    const sensor_msgs::msg::Imu_<ContainerAllocator> & _arg)
  {
    this->imu = _arg;
    return *this;
  }
  Type & set__mag_field(
    const sensor_msgs::msg::MagneticField_<ContainerAllocator> & _arg)
  {
    this->mag_field = _arg;
    return *this;
  }
  Type & set__raw_data(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->raw_data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    imu_msg::msg::ImuMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const imu_msg::msg::ImuMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      imu_msg::msg::ImuMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      imu_msg::msg::ImuMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__imu_msg__msg__ImuMsg
    std::shared_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__imu_msg__msg__ImuMsg
    std::shared_ptr<imu_msg::msg::ImuMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ImuMsg_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->imu != other.imu) {
      return false;
    }
    if (this->mag_field != other.mag_field) {
      return false;
    }
    if (this->raw_data != other.raw_data) {
      return false;
    }
    return true;
  }
  bool operator!=(const ImuMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ImuMsg_

// alias to use template instance with default allocator
using ImuMsg =
  imu_msg::msg::ImuMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace imu_msg

#endif  // IMU_MSG__MSG__DETAIL__IMU_MSG__STRUCT_HPP_
