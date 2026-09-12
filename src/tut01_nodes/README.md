# Lesson 01: nodes, topics, timers

After this lesson you can write a node in Python or C++ that publishes on a
timer, another that subscribes, run them from any of the three ROS 2 package
layouts, and tell from the command line whether two nodes are actually talking.

Prerequisites: none. Time: about an hour.

## Concept

A node is an object. Constructing a `Talker` registers a publisher and a timer
with the middleware, logs "started", and then nothing happens. Callbacks only
run inside `rclpy.spin(node)` or `rclcpp::spin(node)`: spin hands the node to
an executor, which waits for work (a timer expiring, a message arriving) and
calls the matching callback, one at a time, until Ctrl-C. Break-it 1 below
shows a node without spin. It starts, and it exits.

Nodes never talk to each other directly. The talker publishes `std_msgs/String`
on the topic `chatter`; the listener subscribes to `chatter`. Any publisher of
that type on that name reaches every subscriber. The name in the code is
relative, `chatter` and not `/chatter`, so it can be moved into a namespace
later without editing the source (lesson 3). The `10` in
`create_publisher(String, 'chatter', 10)` is the queue depth, the only piece of
QoS you meet here; lesson 5 has the rest.

Both nodes exist in both languages and behave identically:

| | Python | C++ |
|---|---|---|
| node class | [`talker.py`](tut01_nodes/talker.py): `class Talker(Node)` | [`talker.cpp`](src/talker.cpp): `class Talker : public rclcpp::Node` |
| timer | `create_timer(period, cb)`, follows the node clock | `create_wall_timer(period, cb)`, follows the system clock |
| callback | a bound method, `self._on_timer` | a lambda, `[this]() {on_timer();}`; [`listener.cpp`](src/listener.cpp) shows `std::bind` once, for recognition |
| shutdown | `try_shutdown()` in `finally`, catching `ExternalShutdownException` | `rclcpp::shutdown()` after `spin` returns |

The talker reads two parameters, `publish_period` and `greeting`, once at
startup. Lesson 4 is about parameters. Here they exist so that
`--ros-args -p publish_period:=0.1` gives you something to turn.

### The three package layouts

This lesson ships the same two nodes three times, because the layouts are the
content. Every later lesson uses the combined one.

| | [`tut01_nodes_py`](../tut01_nodes_py/README.md) | [`tut01_nodes_cpp`](../tut01_nodes_cpp/README.md) | `tut01_nodes` (this package) |
|---|---|---|---|
| build type | `ament_python` | `ament_cmake` | `ament_cmake` plus `ament_cmake_python` |
| entry point declared in | `setup.py`, `console_scripts` | `CMakeLists.txt`, `add_executable` | both: `add_executable` and `install(PROGRAMS scripts/...)` |
| `ros2 run` finds it at | `install/tut01_nodes_py/lib/tut01_nodes_py/talker` | `install/tut01_nodes_cpp/lib/tut01_nodes_cpp/talker` | `install/tut01_nodes/lib/tut01_nodes/talker_py`, `talker_cpp` |
| `--symlink-install` | source tree linked (an `egg-link`) | nothing to link; edit, rebuild | Python module directory linked, C++ rebuilt |
| lint | pytest files in `test/` | `ament_lint_auto` from CMake | `ament_lint_auto`, both languages |

## Expected output

```bash
colcon build --symlink-install --packages-select tut01_nodes tut01_nodes_py tut01_nodes_cpp
source install/setup.bash
```

Two terminals, each with `install/setup.bash` sourced:

```bash
ros2 run tut01_nodes talker_py
```
```text
[INFO] [talker]: talker started, publishing every 1.0 s
[INFO] [talker]: publishing "hello #0"
[INFO] [talker]: publishing "hello #1"
[INFO] [talker]: publishing "hello #2"
```

```bash
ros2 run tut01_nodes listener_cpp
```
```text
[INFO] [listener]: listener started
[INFO] [listener]: I heard: "hello #0"
[INFO] [listener]: I heard: "hello #1"
[INFO] [listener]: I heard: "hello #2"
```

Swap the suffixes (`talker_cpp`, `listener_py`), or run
`ros2 run tut01_nodes_py talker` and `ros2 run tut01_nodes_cpp listener`. The
output does not change. In a third terminal:

```bash
ros2 node list
ros2 topic list -t
ros2 topic hz /chatter
```
```text
/listener
/talker
/chatter [std_msgs/msg/String]
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
average rate: 1.000
```

## Break it on purpose

Change one thing, watch, read the one-sentence why. Every output below was
captured, not predicted.

1. **No spin.** In `tut01_nodes/talker.py`, comment out `rclpy.spin(node)` and
   run `talker_py`.
   ```text
   [INFO] [talker]: talker started, publishing every 1.0 s
   ```
   Then the process exits. The timer exists, but nothing ever asked an
   executor to run it. Callbacks are not threads; they run only while
   something spins.

2. **Two nodes with one name.** Start `talker_cpp` twice, the second with
   `--ros-args -p greeting:=second`, and a listener.
   ```text
   $ ros2 node list
   WARNING: Be aware that there are nodes in the graph that share an exact name, which can have unintended side effects.
   /listener
   /talker
   /talker
   ```
   The listener prints both streams interleaved: `"second #0"`, `"hello #0"`,
   `"second #1"`. ROS 2 does not stop you. Parameters, services and lifecycle
   transitions (lessons 4, 2, 12) address a node by name, and two of them is a
   bug you will meet later. The fix at startup: `--ros-args -r __node:=talker2`.

3. **Remap the listener's topic.** With a talker running:
   `ros2 run tut01_nodes listener_py --ros-args -r chatter:=chatter2`. The
   listener prints "started" and then nothing.
   ```text
   $ ros2 topic info -v /chatter
   Type: std_msgs/msg/String
   Publisher count: 1
   ...
   Subscription count: 0
   ```
   `ros2 topic list` now shows both `/chatter` and `/chatter2`. Names are
   resolved once, at startup, from `--ros-args`. That is why the source says
   `chatter` and never `/chatter`.

4. **Right name, wrong type.** With talker and listener running:
   `ros2 topic pub -r 2 /chatter std_msgs/msg/Int32 "{data: 1}"`. The listener
   keeps printing `hello #N` and never sees an integer. The publisher prints no
   warning either.
   ```text
   $ ros2 topic list -t
   /chatter [std_msgs/msg/Int32, std_msgs/msg/String]
   ```
   `ros2 topic info -v /chatter` lists two publishers with two types. A topic
   name is a string; types are matched per publisher and subscription pair,
   silently. When "nothing arrives", this is the command to run first.

5. **Edit without rebuilding.** Change the `greeting` default from `'hello'` to
   `'hola'` in all three packages, then run each talker again with no
   `colcon build`:
   ```text
   $ ros2 run tut01_nodes talker_py       # combined
   [INFO] [talker]: publishing "hola #0"
   $ ros2 run tut01_nodes_py talker       # pure Python
   [INFO] [talker]: publishing "hola #0"
   $ ros2 run tut01_nodes_cpp talker      # pure C++
   [INFO] [talker]: publishing "hello #0"
   ```
   `--symlink-install` links Python sources into `install/`. C++ is compiled;
   the binary is whatever it was at the last build. Revert the edit afterwards.

## Node graph

```mermaid
graph LR
  talker -->|"/chatter (std_msgs/String)"| listener
```

## CLI cheat sheet

| Command | What you learn from it |
|---|---|
| `ros2 run <pkg> <exe>` | runs one executable from `install/<pkg>/lib/<pkg>/` |
| `ros2 node list` | who is alive, and whether two share a name |
| `ros2 node info /talker` | that node's publishers, subscriptions, services |
| `ros2 topic list -t` | every topic with its type, or types |
| `ros2 topic echo /chatter` | the messages as the middleware sees them |
| `ros2 topic hz /chatter` | measured publish rate |
| `ros2 topic info -v /chatter` | every publisher and subscription with type and QoS; first stop when nothing arrives |
| `ros2 topic pub -r 2 /chatter std_msgs/msg/String "{data: hi}"` | inject messages from the shell |
| `--ros-args -r chatter:=other` | remap a topic at startup |
| `--ros-args -r __node:=talker2` | rename the node at startup |
| `--ros-args -p publish_period:=0.1` | set a parameter at startup |
| `--ros-args --log-level debug` | more output from rclcpp or rclpy itself |

## In the wild

Each link was opened and checked while writing this lesson.

- [`demo_nodes_cpp/src/topics/talker.cpp`](https://github.com/ros2/demos/blob/jazzy/demo_nodes_cpp/src/topics/talker.cpp)
  and [`listener.cpp`](https://github.com/ros2/demos/blob/jazzy/demo_nodes_cpp/src/topics/listener.cpp):
  the canonical pair. Both use lambdas. The listener's callback takes
  `std_msgs::msg::String::ConstSharedPtr` rather than `const &`; the
  [C++ notes](../../docs/cpp-notes.md#lesson-01-nodes) say why that exists.
- [`publisher_member_function.py`](https://github.com/ros2/examples/blob/jazzy/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py):
  the rclpy pattern this talker follows. It ends with a bare
  `rclpy.shutdown()`, the older idiom that raises if Ctrl-C already shut the
  context down.
- [`tf2_geometry_msgs/CMakeLists.txt`](https://github.com/ros2/geometry2/blob/jazzy/tf2_geometry_msgs/CMakeLists.txt):
  a combined package in production. `ament_python_install_package(${PROJECT_NAME}
  PACKAGE_DIR src/${PROJECT_NAME})` next to a C++ library and a gtest.
- [`cv_bridge/CMakeLists.txt`](https://github.com/ros-perception/vision_opencv/blob/rolling/cv_bridge/CMakeLists.txt):
  same idea, Python under `python/`, C++ under `src/`, with a CMake option to
  leave the Python half out.

## Exercises

Solutions live in [`solution/`](solution/README.md). Build them with
`--cmake-args -DTUT_BUILD_SOLUTIONS=ON --no-warn-unused-cli`.

1. **`relay`.** A node that subscribes to `chatter` and republishes each
   message upper-cased on `chatter_upper`. One node, one subscription, one
   publisher. Check it with `ros2 topic echo /chatter_upper`.
2. **`rate_listener`.** Count messages in the subscription callback and, every
   5 seconds from a timer callback, log the measured rate from
   `get_clock().now()` differences. Two callbacks share one counter; decide
   whether that needs protecting here, and say why.
3. **Periods.** Run the talker with `-p publish_period:=0.1` and confirm with
   `ros2 topic hz`. Then try `0.0`. Write down what you expect before running
   it, then explain what actually happened.
