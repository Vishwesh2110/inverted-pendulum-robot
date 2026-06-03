import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import numpy as np
import time

class PendulumController(Node):

    def __init__(self):
        super().__init__('pendulum_controller')

        self.Kp = 25.0
        self.Ki = 0.5
        self.Kd = 10.0

        self.integral   = 0.0
        self.prev_error = 0.0
        self.prev_time  = time.time()

        self.subscription = self.create_subscription(
            Float64,
            '/pendulum/angle',
            self.angle_callback,
            10
        )

        self.control_publisher = self.create_publisher(
            Float64,
            '/pendulum/control',
            10
        )

        self.get_logger().info('PID Controller started!')

    def angle_callback(self, msg):

        # ── CONVERT DEGREES TO RADIANS ──────────────
        angle_deg = msg.data
        angle_rad = np.radians(angle_deg)   # ← KEY FIX

        # ── TIME STEP ────────────────────────────────
        current_time = time.time()
        dt = current_time - self.prev_time
        if dt <= 0 or dt > 1.0:
            dt = 0.02
        self.prev_time = current_time

        # ── PID (all in radians now) ──────────────────
        error = 0.0 - angle_rad             # target is 0 radians

        P = self.Kp * error

        self.integral += error * dt
        I = self.Ki * self.integral

        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative
        self.prev_error = error

        control = P + I + D
        control = max(-200.0, min(200.0, control))   # bigger clamp

        # ── PUBLISH ───────────────────────────────────
        msg_out = Float64()
        msg_out.data = control
        self.control_publisher.publish(msg_out)

        # ── LOG ───────────────────────────────────────
        self.get_logger().info(
            f'Angle: {angle_deg:7.2f} deg | '
            f'Error_rad: {error:5.3f} | '
            f'P: {P:7.2f} | '
            f'Control: {control:7.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PendulumController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()