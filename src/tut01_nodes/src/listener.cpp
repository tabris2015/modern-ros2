// Copyright 2026 Jose Laruta

#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

/// Subscribes to `chatter` and logs each message.
class Listener : public rclcpp::Node
{
public:
  Listener()
  : Node("listener")
  {
    // std::bind is the older way to turn a member function into a callback.
    // It appears once in these lessons, here, because most ROS 2 code you will
    // read uses it. Everywhere else a lambda does the same job.
    sub_ = create_subscription<std_msgs::msg::String>(
      "chatter", 10, std::bind(&Listener::on_message, this, std::placeholders::_1));
    RCLCPP_INFO(get_logger(), "listener started");
  }

private:
  /// Log one received message.
  void on_message(const std_msgs::msg::String & msg)
  {
    RCLCPP_INFO(get_logger(), "I heard: \"%s\"", msg.data.c_str());
  }

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Listener>());
  rclcpp::shutdown();
  return 0;
}
