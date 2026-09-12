# Copyright 2026 Jose Laruta
"""Exercise 2: measure the rate of `chatter` and log it every 5 seconds."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class RateListener(Node):
    """Counts messages in a subscription callback, reports from a timer callback."""

    def __init__(self) -> None:
        super().__init__('rate_listener')
        self._count = 0
        self._window_start = self.get_clock().now()
        # Both callbacks run on the same thread (single-threaded executor), so
        # the counter needs no lock. Lesson 6 revisits this.
        self._sub = self.create_subscription(String, 'chatter', self._on_message, 10)
        self._timer = self.create_timer(5.0, self._on_timer)
        self.get_logger().info('rate_listener started')

    def _on_message(self, msg: String) -> None:
        """Count one message; the content does not matter here."""
        self._count += 1

    def _on_timer(self) -> None:
        """Log the rate over the last window and start a new one."""
        window_end = self.get_clock().now()
        elapsed = (window_end - self._window_start).nanoseconds / 1e9
        rate = self._count / elapsed if elapsed > 0.0 else 0.0
        self.get_logger().info(f'{self._count} messages in {elapsed:.1f} s: {rate:.2f} Hz')
        self._count = 0
        self._window_start = window_end


def main(args: list[str] | None = None) -> None:
    """Entry point: init, spin, and shut down cleanly."""
    rclpy.init(args=args)
    node = RateListener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
