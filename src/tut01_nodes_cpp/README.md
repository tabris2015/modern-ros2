# tut01_nodes_cpp

The lesson 1 `talker` and `listener` as a pure C++ package (`ament_cmake`).
The lesson itself is [`tut01_nodes`](../tut01_nodes/README.md); this package
exists so you can see this layout build, install, and run.

## What is different here

| | `tut01_nodes_cpp` (this) | `tut01_nodes` (combined) |
|---|---|---|
| Build type | `ament_cmake` only | `ament_cmake` plus `ament_cmake_python` |
| Entry point | `add_executable(talker src/talker.cpp)` | same, target named `talker_cpp` |
| Installed as | `install/tut01_nodes_cpp/lib/tut01_nodes_cpp/talker` | `install/tut01_nodes/lib/tut01_nodes/talker_cpp` |
| Python | none, no `ament_python_install_package`, no `scripts/` | module plus entry scripts |
| Lint | `ament_lint_auto` (cpplint, uncrustify, cppcheck, lint_cmake, xmllint) | same, plus flake8 and pep257 on the Python |
| `--symlink-install` | no effect on C++; edit, rebuild, run | Python linked, C++ rebuilt |

The source files are identical to the combined package's `src/`.

```bash
ros2 run tut01_nodes_cpp talker
ros2 run tut01_nodes_cpp listener
```
