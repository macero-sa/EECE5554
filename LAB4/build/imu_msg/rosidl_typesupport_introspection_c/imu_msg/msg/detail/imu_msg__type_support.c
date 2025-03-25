// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from imu_msg:msg/ImuMsg.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "imu_msg/msg/detail/imu_msg__rosidl_typesupport_introspection_c.h"
#include "imu_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "imu_msg/msg/detail/imu_msg__functions.h"
#include "imu_msg/msg/detail/imu_msg__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `imu`
#include "sensor_msgs/msg/imu.h"
// Member `imu`
#include "sensor_msgs/msg/detail/imu__rosidl_typesupport_introspection_c.h"
// Member `mag_field`
#include "sensor_msgs/msg/magnetic_field.h"
// Member `mag_field`
#include "sensor_msgs/msg/detail/magnetic_field__rosidl_typesupport_introspection_c.h"
// Member `raw_data`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  imu_msg__msg__ImuMsg__init(message_memory);
}

void imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_fini_function(void * message_memory)
{
  imu_msg__msg__ImuMsg__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[4] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msg__msg__ImuMsg, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "imu",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msg__msg__ImuMsg, imu),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mag_field",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msg__msg__ImuMsg, mag_field),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "raw_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(imu_msg__msg__ImuMsg, raw_data),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_members = {
  "imu_msg__msg",  // message namespace
  "ImuMsg",  // message name
  4,  // number of fields
  sizeof(imu_msg__msg__ImuMsg),
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array,  // message members
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_init_function,  // function to initialize message memory (memory has to be allocated)
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle = {
  0,
  &imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_imu_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, imu_msg, msg, ImuMsg)() {
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Imu)();
  imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, MagneticField)();
  if (!imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle.typesupport_identifier) {
    imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &imu_msg__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
