# Copyright 2026 Jose Laruta
"""Publish a greeting on the `chatter` topic at a fixed rate."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    """Publishes "<greeting> #<n>" on `chatter` every `publish_period` seconds."""

    def __init__(self) -> None:
        super().__init__('talker')
        # Parameters are used here and explained in lesson 4.
        self.declare_parameter('publish_period', 1.0)
        self.declare_parameter('greeting', 'hello')
        period: float = self.get_parameter('publish_period').value
        self._greeting: str = self.get_parameter('greeting').value

        self._count = 0
        self._pub = self.create_publisher(String, 'chatter', 10)
        # rclpy timers follow the node clock; there is no separate wall timer.
        self._timer = self.create_timer(period, self._on_timer)
        self.get_logger().info(f'talker started, publishing every {period} s')

    def _on_timer(self) -> None:
        """Publish the next message and log it."""
        msg = String()
        msg.data = f'{self._greeting} #{self._count}'
        self._pub.publish(msg)
        self.get_logger().info(f'publishing "{msg.data}"')
        self._count += 1


def main(args: list[str] | None = None) -> None:
    """Entry point: init, spin, and shut down cleanly."""
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
