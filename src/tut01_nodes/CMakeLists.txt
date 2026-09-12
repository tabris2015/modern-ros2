cmake_minimum_required(VERSION 3.8)
project(tut01_nodes)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Exercise solutions live in solution/ and are off by default:
#   colcon build --cmake-args -DTUT_BUILD_SOLUTIONS=ON
option(TUT_BUILD_SOLUTIONS "Build exercise solutions" OFF)

# ---------- Dependencies ----------
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# ---------- C++ nodes ----------
add_executable(talker_cpp src/talker.cpp)
target_link_libraries(talker_cpp rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(listener_cpp src/listener.cpp)
target_link_libraries(listener_cpp rclcpp::rclcpp ${std_msgs_TARGETS})

install(TARGETS
  talker_cpp
  listener_cpp
  DESTINATION lib/${PROJECT_NAME}
)

# ---------- Python nodes ----------
# Installs the tut01_nodes/ directory as an importable module. The scripts are
# the ros2 run entry points; each imports main() from that module.
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/talker_py
  scripts/listener_py
  DESTINATION lib/${PROJECT_NAME}
)

# ---------- Exercise solutions ----------
if(TUT_BUILD_SOLUTIONS)
  add_executable(relay_cpp solution/src/relay.cpp)
  target_link_libraries(relay_cpp rclcpp::rclcpp ${std_msgs_TARGETS})

  add_executable(rate_listener_cpp solution/src/rate_listener.cpp)
  target_link_libraries(rate_listener_cpp rclcpp::rclcpp ${std_msgs_TARGETS})

  install(TARGETS
    relay_cpp
    rate_listener_cpp
    DESTINATION lib/${PROJECT_NAME}
  )

  ament_python_install_package(${PROJECT_NAME}_solution
    PACKAGE_DIR solution/${PROJECT_NAME}_solution
  )

  install(PROGRAMS
    solution/scripts/relay_py
    solution/scripts/rate_listener_py
    DESTINATION lib/${PROJECT_NAME}
  )
endif()

# ---------- Testing ----------
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # Source files carry a one-line copyright, not the full license block
  # ament_copyright wants. cpplint still checks that the line exists.
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
