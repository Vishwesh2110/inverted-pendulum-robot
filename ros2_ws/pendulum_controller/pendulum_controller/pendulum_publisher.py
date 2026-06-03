# ============================================================
# FILE: pendulum_publisher.py
# WHAT: A ROS 2 node that simulates pendulum angle and
#       publishes it to a topic called /pendulum/angle
# WHY:  This is how robot sensors share data in ROS
# ============================================================

import rclpy                          # ROS 2 Python library
from rclpy.node import Node           # base class for all nodes
from std_msgs.msg import Float64      # message type (a single number)
import numpy as np
import time

class PendulumPublisher(Node):
    """
    This class IS your ROS node.
    It simulates pendulum physics and broadcasts
    the angle every 0.02 seconds.
    """

    def __init__(self):
        # Give this node a name — ROS uses this to identify it
        super().__init__('pendulum_publisher')

        # CREATE A PUBLISHER
        # - publishes Float64 messages
        # - on topic named '/pendulum/angle'
        # - queue size 10 (holds 10 messages if receiver is slow)
        self.publisher_ = self.create_publisher(
            Float64,
            '/pendulum/angle',
            10
        )

        # PENDULUM PHYSICS STATE
        self.theta     = np.radians(5.0)   # start tilted 5 degrees
        self.theta_dot = 0.0               # start at rest
        self.dt        = 0.02              # time step (seconds)
        self.g         = 9.81
        self.L         = 1.0

        # CREATE A TIMER
        # Calls self.timer_callback every 0.02 seconds
        self.get_logger().info('Waiting 3 seconds for subscriber to connect...')
        time.sleep(3)
        self.get_logger().info('Starting physics now!')
        self.timer = self.create_timer(self.dt, self.timer_callback)
        self.get_logger().info('Pendulum Publisher started!')

    def timer_callback(self):
        """
        This function runs every 0.02 seconds automatically.
        It updates the physics and publishes the new angle.
        """

        # UPDATE PHYSICS (no control — free fall)
        theta_dotdot   = (self.g / self.L) * np.sin(self.theta)
        self.theta_dot += theta_dotdot * self.dt
        self.theta     += self.theta_dot * self.dt

        # CREATE MESSAGE and publish
        msg = Float64()
        msg.data = float(np.degrees(self.theta))  # convert to degrees

        self.publisher_.publish(msg)

        # LOG to terminal every callback
        self.get_logger().info(
            f'Publishing angle: {msg.data:.2f} degrees'
        )


def main(args=None):
    rclpy.init(args=args)                  # start ROS 2
    node = PendulumPublisher()             # create our node
    rclpy.spin(node)                       # keep it running
    node.destroy_node()                    # cleanup
    rclpy.shutdown()                       # stop ROS 2


if __name__ == '__main__':
    main()