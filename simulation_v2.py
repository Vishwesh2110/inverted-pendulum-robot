import numpy as np
import matplotlib.pyplot as plt

g    = 9.81
L    = 1.0
dt   = 0.02
t_end = 5.0

Kp = 25.0
Ki = 0.5
Kd = 10.0

def simulate(use_pid, start_angle_deg=5.0):
    theta      = np.radians(start_angle_deg)
    theta_dot  = 0.0
    integral   = 0.0
    prev_error = 0.0
    time_list  = []
    angle_list = []
    t = 0

    while t <= t_end:
        error = 0.0 - theta

        if use_pid:
            P          = Kp * error
            integral  += error * dt
            I          = Ki * integral
            derivative = (error - prev_error) / dt
            D          = Kd * derivative
            control    = np.clip(P + I + D, -50, 50)
            prev_error = error
        else:
            control = 0.0

        theta_dotdot = (g / L) * np.sin(theta) + control
        theta_dot   += theta_dotdot * dt
        theta        += theta_dot * dt

        time_list.append(t)
        angle_list.append(np.degrees(theta))
        t += dt

    return time_list, angle_list

print("Running WITHOUT PID...")
t_no, a_no = simulate(use_pid=False)

print("Running WITH PID...")
t_pid, a_pid = simulate(use_pid=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(t_no, a_no, color='red', linewidth=2)
ax1.axhline(y=0, color='green', linestyle='--')
ax1.set_title('No Control - Pendulum Falls')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Tilt Angle (degrees)')
ax1.grid(True)

ax2.plot(t_pid, a_pid, color='blue', linewidth=2)
ax2.axhline(y=0, color='green', linestyle='--', label='Target 0 degrees')
ax2.set_title('With PID - Pendulum Balances!')
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Tilt Angle (degrees)')
ax2.set_ylim(-15, 15)
ax2.legend()
ax2.grid(True)

plt.suptitle('Inverted Pendulum: Before vs After PID', fontweight='bold')
plt.tight_layout()
plt.savefig('pid_comparison.png')

print(f"Without PID --> Final angle: {a_no[-1]:.1f} degrees")
print(f"With PID    --> Final angle: {a_pid[-1]:.4f} degrees")
print("Saved: pid_comparison.png")