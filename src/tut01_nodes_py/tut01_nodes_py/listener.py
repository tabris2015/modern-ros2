# Copyright 2026 Jose Laruta
"""Print every message received on the `chatter` topic."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    """Subscribes to `chatter` and logs each message."""

    def __init__(self) -> None:
        super().__init__('listener')
        self._sub = self.create_subscription(String, 'chatter', self._on_message, 10)
        self.get_logger().info('listener started')

    def _on_message(self, msg: String) -> None:
        """Log one received message."""
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args: list[str] | None = None) -> None:
    """Entry point: init, spin, and shut down cleanly."""
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
