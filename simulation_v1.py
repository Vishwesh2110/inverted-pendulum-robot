# ============================================================
# FILE: simulation_v1.py
# WHAT: Simulates an inverted pendulum falling over with no control
# WHY:  This shows us WHAT we are trying to prevent
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ── PHYSICS CONSTANTS ──────────────────────────────────────
g = 9.81        # gravity (m/s²) — pulls pendulum down
L = 1.0         # length of pendulum rod (meters)
m = 1.0         # mass at top of pendulum (kg)
dt = 0.02       # time step (seconds) — how often we update physics
t_end = 3.0     # total simulation time (seconds)

# ── STARTING CONDITIONS ────────────────────────────────────
# Angle is measured from the vertical (straight up = 0 degrees)
# We start slightly tilted — 5 degrees converted to radians
theta = np.radians(5)    # starting angle (small tilt)
theta_dot = 0.0          # starting angular velocity (not moving yet)

# ── STORAGE (to save history for plotting) ─────────────────
time_list  = []
angle_list = []

# ── SIMULATION LOOP ────────────────────────────────────────
# This loop runs the physics forward in tiny time steps
t = 0
while t <= t_end:

    # PHYSICS EQUATION of inverted pendulum (no control force)
    # theta_dotdot = how fast the tilt is ACCELERATING
    # gravity constantly pulls the top mass outward
    theta_dotdot = (g / L) * np.sin(theta)

    # Update velocity and angle using the acceleration
    theta_dot = theta_dot + theta_dotdot * dt   # new angular speed
    theta     = theta + theta_dot * dt           # new angle

    # Save values for plotting
    time_list.append(t)
    angle_list.append(np.degrees(theta))  # convert back to degrees

    t += dt  # move time forward

# ── PLOT THE RESULT ────────────────────────────────────────
plt.figure(figsize=(10, 5))

plt.plot(time_list, angle_list, color='red', linewidth=2)

plt.axhline(y=0,   color='green', linestyle='--', linewidth=1, label='Balanced (0°)')
plt.axhline(y=90,  color='gray',  linestyle=':',  linewidth=1, label='Fallen over (90°)')

plt.title('Inverted Pendulum — NO CONTROL (It Falls!)', fontsize=14)
plt.xlabel('Time (seconds)')
plt.ylabel('Tilt Angle (degrees)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('pendulum_falling.png')   # saves graph as image file
print("Graph saved as pendulum_falling.png")
print(f"Final angle: {angle_list[-1]:.1f} degrees — it fell over!")