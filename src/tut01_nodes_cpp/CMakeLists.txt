cmake_minimum_required(VERSION 3.8)
project(tut01_nodes_cpp)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(talker src/talker.cpp)
target_link_libraries(talker rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(listener src/listener.cpp)
target_link_libraries(listener rclcpp::rclcpp ${std_msgs_TARGETS})

# ros2 run looks for executables under lib/<package>.
install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # Source files carry a one-line copyright, not the full license block
  # ament_copyright wants. cpplint still checks that the line exists.
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
