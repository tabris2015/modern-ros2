# Lesson 01 solutions

Try the exercises before reading these.

C++ in `src/`, Python in `tut01_nodes_solution/` (installed as that module),
entry scripts in `scripts/`. Everything here is linted with the lesson; it only
builds when you ask:

```bash
colcon build --symlink-install --packages-select tut01_nodes \
  --cmake-args -DTUT_BUILD_SOLUTIONS=ON --no-warn-unused-cli
source install/setup.bash
```

## Exercise 1: relay

[`relay.py`](tut01_nodes_solution/relay.py), [`relay.cpp`](src/relay.cpp).
One node holds both a subscription and a publisher, and publishes from inside
the subscription callback. That is normal; a callback may do anything a node
can do. Whether the publisher or the subscription is created first does not
matter.

```bash
ros2 run tut01_nodes talker_py
ros2 run tut01_nodes relay_cpp
ros2 topic echo /chatter_upper
```
```text
data: 'HELLO #1'
---
data: 'HELLO #2'
```

## Exercise 2: rate_listener

[`rate_listener.py`](tut01_nodes_solution/rate_listener.py),
[`rate_listener.cpp`](src/rate_listener.cpp). Two callbacks, the subscription
and a 5 s timer, share one counter. With the default single-threaded executor
they can never run at the same time, so there is nothing to lock. Lesson 6
changes that assumption on purpose.

Time comes from `get_clock().now()`, which is ROS time (it follows simulated
time in lesson 9). Subtracting two `rclcpp::Time` values gives a
`rclcpp::Duration` with `.seconds()`; in rclpy the difference has
`.nanoseconds`.

```text
[INFO] [rate_listener]: 5 messages in 5.0 s: 1.00 Hz
```

The first window sometimes reports 4 messages: the window opened before the
talker published its first one.

## Exercise 3: publish_period 0.1 and 0.0

`-p publish_period:=0.1` gives `ros2 topic hz /chatter` about 10 Hz (measured
9.996).

`-p publish_period:=0.0` is accepted by both rclpy and rclcpp without complaint,
and the timer then fires every time the executor loops. Measured inside the
devcontainer over two seconds: about 4,400 messages from the Python talker and
about 27,500 from the C++ one, each with a log line. A zero-period timer is a
busy loop. If a node needs to publish as fast as it can, drive it from the data
that arrives (a subscription callback) or run your own loop with `spin_some`,
rather than asking a timer to fire continuously.
