# tut01_nodes_py

The lesson 1 `talker` and `listener` as a pure Python package (`ament_python`).
The lesson itself is [`tut01_nodes`](../tut01_nodes/README.md); this package
exists so you can see this layout build, install, and run.

## What is different here

| | `tut01_nodes_py` (this) | `tut01_nodes` (combined) |
|---|---|---|
| Build type | `ament_python`: colcon runs `setup.py`, no CMake | `ament_cmake` plus `ament_cmake_python` |
| Entry point | `setup.py` `console_scripts`, `talker = tut01_nodes_py.talker:main` | `scripts/talker_py`, installed with `install(PROGRAMS ...)` |
| Installed as | `install/tut01_nodes_py/lib/tut01_nodes_py/talker` | `install/tut01_nodes/lib/tut01_nodes/talker_py` |
| Lint | pytest files in `test/` (flake8, pep257; copyright skipped) | `ament_lint_auto`, driven from CMake |
| `--symlink-install` | the source tree is linked; edits apply without a rebuild | Python linked, C++ rebuilt |
| Needs `setup.cfg` | yes, so `ros2 run` finds scripts under `lib/<pkg>` | no |

The node code is identical to the combined package's, only the module name
changes (`tut01_nodes_py.talker` instead of `tut01_nodes.talker`).

```bash
ros2 run tut01_nodes_py talker
ros2 run tut01_nodes_py listener
```
