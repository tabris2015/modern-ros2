# C++ notes

Language explanations for the C++ side of each lesson, kept out of the lesson
READMEs so those stay about ROS 2. One section per lesson. Read it after the
lesson, once the constructs have context.

## Lesson 01: nodes

Files: [`src/tut01_nodes/src/talker.cpp`](../src/tut01_nodes/src/talker.cpp),
[`src/tut01_nodes/src/listener.cpp`](../src/tut01_nodes/src/listener.cpp).

### `std::shared_ptr`, `std::make_shared`, and the `::SharedPtr` aliases

`rclcpp::spin(std::make_shared<Talker>())` builds the node on the heap and hands
a shared pointer to the executor. rclcpp uses shared ownership everywhere
because the middleware holds references to your objects too: the executor to
the node, the node to its publishers and timers. Every rclcpp class exposes
aliases for this, so `rclcpp::Publisher<std_msgs::msg::String>::SharedPtr` is
`std::shared_ptr<rclcpp::Publisher<std_msgs::msg::String>>` with less typing.

The gotcha: the member variable is the owner. Drop `timer_` from the class and
keep the `create_wall_timer` call, and the timer is destroyed at the end of the
constructor. No error, no warning, no callbacks.

### Deriving from `rclcpp::Node`

`class Talker : public rclcpp::Node` with the constructor initializer list
`: Node("talker")`. The base constructor needs the node name, so it has to be
called there, before the body runs. Public inheritance makes
`create_publisher`, `create_wall_timer`, `declare_parameter`, `get_logger` plain
member calls. Older code writes `this->create_publisher(...)`; both forms mean
the same thing.

### Lambdas capturing `[this]`

`[this]() {on_timer();}` is a closure that stores a pointer to the node and
calls a member function through it. It is safe here because the node owns the
timer: the timer, and with it the closure, is destroyed with the node, so the
stored `this` never outlives the object. The solutions use the one-argument
form, `[this](const std_msgs::msg::String & msg) {on_message(msg);}`, for a
subscription callback.

### `std::bind` and `std::placeholders::_1`

`std::bind(&Listener::on_message, this, std::placeholders::_1)` produces a
callable that forwards its first argument to `on_message` on `this`. It does
exactly what the lambda does, with a worse error message when the signature is
wrong. Most ROS 2 code written before lambdas were idiomatic uses it, so you
need to read it; you do not need to write it.

### `std::chrono_literals` and `std::chrono::duration<double>`

`using namespace std::chrono_literals;` enables `1s`, `500ms`, `5s`. A period
that comes from a parameter at runtime cannot be a literal, so `talker.cpp`
wraps it: `std::chrono::duration<double>(period)` is a duration counted in
seconds with a `double` tick. `create_wall_timer` is a template over the
duration type and converts to nanoseconds itself.

### Callback parameter: `const T &` versus `T::SharedPtr`

rclcpp accepts several subscription callback signatures. `const T & msg` is the
simplest and what the lesson uses. `T::ConstSharedPtr` (what the `ros2/demos`
listener uses) and `std::unique_ptr<T>` exist for a reason: with intra-process
communication they let the middleware hand you the message without copying.
That is lesson 13. Until then, `const T &`.

### `RCLCPP_INFO` versus `RCLCPP_INFO_STREAM`

`RCLCPP_INFO(get_logger(), "publishing \"%s\"", msg.data.c_str())` is
printf-style. A `std::string` passed to `%s` is undefined behaviour, hence
`.c_str()`; the compiler warns about it under `-Wall`. `RCLCPP_INFO_STREAM`
takes `<<` expressions instead. Both are macros that check the log level before
formatting anything.

### `int count_{0};` and `count_++` inside an expression

Default member initializers keep the constructor body about ROS, not about
zeroing fields. `std::to_string(count_++)` evaluates to the old value and then
increments, which is the whole reason the messages start at `#0`.

### `main`: `rclcpp::init`, `spin`, `shutdown`

`init(argc, argv)` parses `--ros-args` (remaps, parameters, log level) and
installs a SIGINT handler. `spin` blocks, running a single-threaded executor
over the node until Ctrl-C triggers shutdown. `shutdown` tears the context down.
Python has the same three steps with `try_shutdown` guarding the case where
Ctrl-C already did it.
