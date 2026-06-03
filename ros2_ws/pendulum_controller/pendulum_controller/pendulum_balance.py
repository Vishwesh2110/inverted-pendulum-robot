# ============================================================
# FILE: pendulum_balance.py
# WHAT: Single ROS node — physics + PID in one timer loop
# WHY:  Eliminates timing delay between two separate nodes
#       This is how real robot controllers work
# ============================================================

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import numpy as np

class PendulumBalance(Node):

    def __init__(self):
        super().__init__('pendulum_balance')

        # ── PHYSICS
        self.theta     = np.radians(5.0)
        self.theta_dot = 0.0
        self.dt        = 0.02
        self.g         = 9.81
        self.L         = 1.0

        # ── PID GAINS
        self.Kp = 25.0
        self.Ki = 0.5
        self.Kd = 10.0

        # ── PID MEMORY
        self.integral   = 0.0
        self.prev_error = 0.0

        # ── PUBLISHERS (so we can monitor with ros2 topic echo)
        self.angle_pub   = self.create_publisher(Float64, '/pendulum/angle', 10)
        self.control_pub = self.create_publisher(Float64, '/pendulum/control', 10)

        # ── TIMER (physics + PID runs every 0.02 seconds)
        self.timer = self.create_timer(self.dt, self.timer_callback)

        self.get_logger().info('Pendulum Balance Node started!')

    def timer_callback(self):

        # ── STEP 1: READ ANGLE (sensor)
        error = 0.0 - self.theta      # error in radians

        # ── STEP 2: RUN PID (controller)
        P = self.Kp * error

        self.integral += error * self.dt
        I = self.Ki * self.integral

        derivative = (error - self.prev_error) / self.dt
        D = self.Kd * derivative
        self.prev_error = error

        control = np.clip(P + I + D, -200.0, 200.0)

        # ── STEP 3: APPLY CONTROL (actuator)
        theta_dotdot    = (self.g / self.L) * np.sin(self.theta) + control
        self.theta_dot += theta_dotdot * self.dt
        self.theta     += self.theta_dot * self.dt

        # ── STEP 4: PUBLISH to topics (for monitoring)
        angle_msg = Float64()
        angle_msg.data = float(np.degrees(self.theta))
        self.angle_pub.publish(angle_msg)

        control_msg = Float64()
        control_msg.data = float(control)
        self.control_pub.publish(control_msg)

        # ── LOG
        self.get_logger().info(
            f'Angle: {np.degrees(self.theta):8.4f} deg | '
            f'Control: {control:8.3f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PendulumBalance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()