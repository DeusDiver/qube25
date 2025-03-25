cmake_minimum_required(VERSION 3.8)
project(pid_controller_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)  # Add this line to find std_msgs

# Generate interfaces (service definition)
rosidl_generate_interfaces(pid_controller_msgs
  "srv/SetReference.srv"
  DEPENDENCIES std_msgs  # Add std_msgs as a dependency for the service
)

# Add testing if needed
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)  # Skip copyright check
  set(ament_cmake_cpplint_FOUND TRUE)  # Skip cpplint check if not in a git repo
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_dependencies(rosidl_default_runtime)
ament_package()
