# Copyright 2026 Jose Laruta
"""Exercise 1: re-publish `chatter` upper-cased on `chatter_upper`."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Relay(Node):
    """One node that is both a subscriber and a publisher."""

    def __init__(self) -> None:
        super().__init__('relay')
        self._pub = self.create_publisher(String, 'chatter_upper', 10)
        self._sub = self.create_subscription(String, 'chatter', self._on_message, 10)
        self.get_logger().info('relay started')

    def _on_message(self, msg: String) -> None:
        """Upper-case one message and publish it."""
        out = String()
        out.data = msg.data.upper()
        self._pub.publish(out)
        self.get_logger().info(f'relayed "{out.data}"')


def main(args: list[str] | None = None) -> None:
    """Entry point: init, spin, and shut down cleanly."""
    rclpy.init(args=args)
    node = Relay()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
