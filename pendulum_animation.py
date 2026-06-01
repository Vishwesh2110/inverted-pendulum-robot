# ============================================================
# FILE: pendulum_animation.py
# WHAT: Real-time animated inverted pendulum with PID control
# WHY:  Visual demo for interviews and GitHub
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ── PHYSICS
g    = 9.81
L    = 1.0
dt   = 0.02

# ── PID GAINS
Kp = 25.0
Ki = 0.5
Kd = 10.0

# ── SIMULATE BOTH (pre-compute all frames)
def simulate(use_pid, start_angle_deg=5.0, t_end=5.0):
    theta      = np.radians(start_angle_deg)
    theta_dot  = 0.0
    integral   = 0.0
    prev_error = 0.0
    angles = []

    t = 0
    while t <= t_end:
        error = -theta
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
        theta       += theta_dot * dt
        angles.append(theta)
        t += dt

    return angles

print("Pre-computing simulation...")
angles_no_pid  = simulate(use_pid=False)
angles_with_pid = simulate(use_pid=True)
n_frames = min(len(angles_no_pid), len(angles_with_pid))
print(f"Ready. Rendering {n_frames} frames...")

# ── BUILD THE FIGURE
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor('#1a1a2e')   # dark background

def style_axis(ax, title):
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_facecolor('#16213e')
    ax.set_title(title, color='white', fontsize=12, fontweight='bold')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#444')
    ax.spines['top'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.spines['right'].set_color('#444')
    # draw ground line
    ax.axhline(y=-1.3, color='#555', linewidth=2)
    # draw target vertical line
    ax.axvline(x=0, color='#2ecc71', linewidth=1,
               linestyle='--', alpha=0.4, label='Target')

style_axis(ax1, 'NO CONTROL  —  Falls Over')
style_axis(ax2, 'PID CONTROL  —  Balances!')

# pivot point (base of pendulum)
pivot = (0, -0.3)

# ── DRAWING ELEMENTS (left panel - no PID)
rod1,  = ax1.plot([], [], 'o-',
                  color='#e74c3c', linewidth=4,
                  markersize=12, markerfacecolor='#e74c3c')
base1, = ax1.plot(*pivot, 's',
                  color='#bdc3c7', markersize=10)
time_text1 = ax1.text(-1.3, 1.3, '', color='white', fontsize=9)
angle_text1 = ax1.text(-1.3, 1.1, '', color='#e74c3c', fontsize=9)

# ── DRAWING ELEMENTS (right panel - with PID)
rod2,  = ax2.plot([], [], 'o-',
                  color='#3498db', linewidth=4,
                  markersize=12, markerfacecolor='#3498db')
base2, = ax2.plot(*pivot, 's',
                  color='#bdc3c7', markersize=10)
time_text2  = ax2.text(-1.3, 1.3, '', color='white', fontsize=9)
angle_text2 = ax2.text(-1.3, 1.1, '', color='#2ecc71', fontsize=9)

plt.tight_layout()

# ── ANIMATION FUNCTION (called every frame)
def update(frame):
    # clamp frame to available data
    i = min(frame, n_frames - 1)

    # ── LEFT: no PID
    theta1 = angles_no_pid[i]
    # pendulum tip position (pivot is origin, rod goes UP)
    x1 = pivot[0] + L * np.sin(theta1)
    y1 = pivot[1] + L * np.cos(theta1)
    rod1.set_data([pivot[0], x1], [pivot[1], y1])
    time_text1.set_text(f'Time:  {i * dt:.1f}s')
    angle_text1.set_text(f'Angle: {np.degrees(theta1):.1f} deg')

    # ── RIGHT: with PID
    theta2 = angles_with_pid[i]
    x2 = pivot[0] + L * np.sin(theta2)
    y2 = pivot[1] + L * np.cos(theta2)
    rod2.set_data([pivot[0], x2], [pivot[1], y2])
    time_text2.set_text(f'Time:  {i * dt:.1f}s')
    angle_text2.set_text(f'Angle: {np.degrees(theta2):.4f} deg')

    return rod1, rod2, time_text1, time_text2, angle_text1, angle_text2

# ── RUN ANIMATION
ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_frames,
    interval=dt * 1000,    # interval in milliseconds
    blit=True,
    repeat=True
)

plt.suptitle('Inverted Pendulum Simulation — PID Control',
             color='white', fontsize=14, fontweight='bold')

print("Showing animation... (close window to exit)")
plt.show()