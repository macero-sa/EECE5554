// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from imu_msg:msg/ImuMsg.idl
// generated code does not contain a copyright notice
#include "imu_msg/msg/detail/imu_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `imu`
#include "sensor_msgs/msg/detail/imu__functions.h"
// Member `mag_field`
#include "sensor_msgs/msg/detail/magnetic_field__functions.h"
// Member `raw_data`
#include "rosidl_runtime_c/string_functions.h"

bool
imu_msg__msg__ImuMsg__init(imu_msg__msg__ImuMsg * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    imu_msg__msg__ImuMsg__fini(msg);
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__init(&msg->imu)) {
    imu_msg__msg__ImuMsg__fini(msg);
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__init(&msg->mag_field)) {
    imu_msg__msg__ImuMsg__fini(msg);
    return false;
  }
  // raw_data
  if (!rosidl_runtime_c__String__init(&msg->raw_data)) {
    imu_msg__msg__ImuMsg__fini(msg);
    return false;
  }
  return true;
}

void
imu_msg__msg__ImuMsg__fini(imu_msg__msg__ImuMsg * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // imu
  sensor_msgs__msg__Imu__fini(&msg->imu);
  // mag_field
  sensor_msgs__msg__MagneticField__fini(&msg->mag_field);
  // raw_data
  rosidl_runtime_c__String__fini(&msg->raw_data);
}

bool
imu_msg__msg__ImuMsg__are_equal(const imu_msg__msg__ImuMsg * lhs, const imu_msg__msg__ImuMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__are_equal(
      &(lhs->imu), &(rhs->imu)))
  {
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__are_equal(
      &(lhs->mag_field), &(rhs->mag_field)))
  {
    return false;
  }
  // raw_data
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->raw_data), &(rhs->raw_data)))
  {
    return false;
  }
  return true;
}

bool
imu_msg__msg__ImuMsg__copy(
  const imu_msg__msg__ImuMsg * input,
  imu_msg__msg__ImuMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // imu
  if (!sensor_msgs__msg__Imu__copy(
      &(input->imu), &(output->imu)))
  {
    return false;
  }
  // mag_field
  if (!sensor_msgs__msg__MagneticField__copy(
      &(input->mag_field), &(output->mag_field)))
  {
    return false;
  }
  // raw_data
  if (!rosidl_runtime_c__String__copy(
      &(input->raw_data), &(output->raw_data)))
  {
    return false;
  }
  return true;
}

imu_msg__msg__ImuMsg *
imu_msg__msg__ImuMsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msg__msg__ImuMsg * msg = (imu_msg__msg__ImuMsg *)allocator.allocate(sizeof(imu_msg__msg__ImuMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(imu_msg__msg__ImuMsg));
  bool success = imu_msg__msg__ImuMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
imu_msg__msg__ImuMsg__destroy(imu_msg__msg__ImuMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    imu_msg__msg__ImuMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
imu_msg__msg__ImuMsg__Sequence__init(imu_msg__msg__ImuMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msg__msg__ImuMsg * data = NULL;

  if (size) {
    data = (imu_msg__msg__ImuMsg *)allocator.zero_allocate(size, sizeof(imu_msg__msg__ImuMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = imu_msg__msg__ImuMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        imu_msg__msg__ImuMsg__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
imu_msg__msg__ImuMsg__Sequence__fini(imu_msg__msg__ImuMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      imu_msg__msg__ImuMsg__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

imu_msg__msg__ImuMsg__Sequence *
imu_msg__msg__ImuMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  imu_msg__msg__ImuMsg__Sequence * array = (imu_msg__msg__ImuMsg__Sequence *)allocator.allocate(sizeof(imu_msg__msg__ImuMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = imu_msg__msg__ImuMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
imu_msg__msg__ImuMsg__Sequence__destroy(imu_msg__msg__ImuMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    imu_msg__msg__ImuMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
imu_msg__msg__ImuMsg__Sequence__are_equal(const imu_msg__msg__ImuMsg__Sequence * lhs, const imu_msg__msg__ImuMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!imu_msg__msg__ImuMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
imu_msg__msg__ImuMsg__Sequence__copy(
  const imu_msg__msg__ImuMsg__Sequence * input,
  imu_msg__msg__ImuMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(imu_msg__msg__ImuMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    imu_msg__msg__ImuMsg * data =
      (imu_msg__msg__ImuMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!imu_msg__msg__ImuMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          imu_msg__msg__ImuMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!imu_msg__msg__ImuMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
