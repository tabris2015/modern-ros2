// Copyright 2026 Jose Laruta

#include <algorithm>
#include <cctype>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

/// Re-publishes each `chatter` message upper-cased on `chatter_upper`.
class Relay : public rclcpp::Node
{
public:
  Relay()
  : Node("relay")
  {
    pub_ = create_publisher<std_msgs::msg::String>("chatter_upper", 10);
    sub_ = create_subscription<std_msgs::msg::String>(
      "chatter", 10, [this](const std_msgs::msg::String & msg) {on_message(msg);});
    RCLCPP_INFO(get_logger(), "relay started");
  }

private:
  /// Upper-case one message and publish it.
  void on_message(const std_msgs::msg::String & msg)
  {
    auto out = std_msgs::msg::String();
    out.data = msg.data;
    std::transform(
      out.data.begin(), out.data.end(), out.data.begin(),
      [](unsigned char c) {return std::toupper(c);});
    pub_->publish(out);
    RCLCPP_INFO(get_logger(), "relayed \"%s\"", out.data.c_str());
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Relay>());
  rclcpp::shutdown();
  return 0;
}
