// Copyright 2026 Jose Laruta

#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

/// Counts `chatter` messages and logs the measured rate every 5 seconds.
class RateListener : public rclcpp::Node
{
public:
  RateListener()
  : Node("rate_listener")
  {
    window_start_ = now();
    // Both callbacks run on the same thread (single-threaded executor), so the
    // counter needs no lock. Lesson 6 revisits this.
    sub_ = create_subscription<std_msgs::msg::String>(
      "chatter", 10, [this](const std_msgs::msg::String &) {++count_;});
    timer_ = create_wall_timer(5s, [this]() {on_timer();});
    RCLCPP_INFO(get_logger(), "rate_listener started");
  }

private:
  /// Log the rate over the last window and start a new one.
  void on_timer()
  {
    const auto window_end = now();
    const double elapsed = (window_end - window_start_).seconds();
    const double rate = elapsed > 0.0 ? count_ / elapsed : 0.0;
    RCLCPP_INFO(get_logger(), "%d messages in %.1f s: %.2f Hz", count_, elapsed, rate);
    count_ = 0;
    window_start_ = window_end;
  }

  int count_{0};
  rclcpp::Time window_start_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<RateListener>());
  rclcpp::shutdown();
  return 0;
}
