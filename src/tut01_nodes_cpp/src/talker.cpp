// Copyright 2026 Jose Laruta

#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

/// Publishes "<greeting> #<n>" on `chatter` every `publish_period` seconds.
class Talker : public rclcpp::Node
{
public:
  Talker()
  : Node("talker")
  {
    // Parameters are used here and explained in lesson 4.
    const auto period = declare_parameter<double>("publish_period", 1.0);
    greeting_ = declare_parameter<std::string>("greeting", "hello");

    pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);
    // A wall timer follows the system clock. The lambda captures `this`; the
    // node owns the timer, so the pointer outlives every call.
    timer_ = create_wall_timer(
      std::chrono::duration<double>(period), [this]() {on_timer();});
    RCLCPP_INFO(get_logger(), "talker started, publishing every %.1f s", period);
  }

private:
  /// Publish the next message and log it.
  void on_timer()
  {
    auto msg = std_msgs::msg::String();
    msg.data = greeting_ + " #" + std::to_string(count_++);
    pub_->publish(msg);
    RCLCPP_INFO(get_logger(), "publishing \"%s\"", msg.data.c_str());
  }

  std::string greeting_;
  int count_{0};
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Talker>());
  rclcpp::shutdown();
  return 0;
}
