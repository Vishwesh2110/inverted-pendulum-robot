# ============================================================
# FILE: gazebo_balance.py
# WHAT: Reads real IMU from Gazebo, runs PID, drives wheels
# WHY:  This is the complete robot controller
# ============================================================

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
import math

class GazeboBalance(Node):

    def __init__(self):
        super().__init__('gazebo_balance')

        # PID GAINS
        self.Kp = 80.0
        self.Ki = 0.3
        self.Kd = 12.0

        # PID MEMORY
        self.integral   = 0.0
        self.prev_error = 0.0
        self.prev_time  = self.get_clock().now()

        # SUBSCRIBE to real IMU sensor
        self.imu_sub = self.create_subscription(
            Imu, '/imu', self.imu_callback, 10)

        # PUBLISH wheel commands
        self.cmd_pub = self.create_publisher(
            Twist, '/cmd_vel', 10)

        self.get_logger().info('Gazebo Balance Controller started!')

    def imu_callback(self, msg):

        # CONVERT quaternion to tilt angle (pitch)
        q = msg.orientation
        # Extract pitch angle from quaternion
        sinp = 2.0 * (q.w * q.y - q.z * q.x)
        sinp = max(-1.0, min(1.0, sinp))
        pitch = math.asin(sinp)   # tilt in radians

        # TIME STEP
        now = self.get_clock().now()
        dt = (now - self.prev_time).nanoseconds / 1e9
        if dt <= 0 or dt > 1.0:
            dt = 0.02
        self.prev_time = now

        # PID
        error = 0.0 - pitch

        P = self.Kp * error

        self.integral += error * dt
        self.integral = max(-2.0, min(2.0, self.integral))
        I = self.Ki * self.integral

        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative
        self.prev_error = error

        control = P + I + D
        control = max(-10.0, min(10.0, control))

        # SEND to wheels
        cmd = Twist()
        cmd.linear.x = control
        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f'Pitch: {math.degrees(pitch):6.3f} deg | '
            f'Control: {control:6.3f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = GazeboBalance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()