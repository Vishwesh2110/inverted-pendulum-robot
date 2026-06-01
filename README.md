# Inverted Pendulum — Self-Balancing Robot Simulation

A physics-based simulation of an inverted pendulum system
controlled by a PID controller. Built from scratch using
Python on Ubuntu Linux.

Phase 1 of a complete self-balancing robot project using
Python, ROS 2, and Gazebo.

## Results
- Uncontrolled pendulum: falls to 354 degrees
- PID controlled pendulum: stabilizes at 0.0002 degrees
- Steady-state error: 0.0002 degrees from 5 degree disturbance

## Physics
    theta'' = (g/L) x sin(theta) + u

- theta = angle from vertical
- g = 9.81 m/s^2
- L = 1.0 m (rod length)
- u = PID control output

## PID Gains

| Gain | Value | Purpose                     |
|------|-------|-----------------------------|
| Kp   | 25.0  | Reacts to current tilt      |
| Ki   | 0.5   | Corrects long-term drift    |
| Kd   | 10.0  | Brakes before overshoot     |

## Files

| File                  | What it does                       |
|-----------------------|------------------------------------|
| simulation_v1.py      | Pendulum with no control (falls)   |
| simulation_v2.py      | Pendulum with PID (balances)       |
| pendulum_animation.py | Live side-by-side animation        |

## How to Run

```bash
pip3 install numpy matplotlib
python3 simulation_v1.py
python3 simulation_v2.py
python3 pendulum_animation.py
```

## Tech Stack
Python 3 · NumPy · Matplotlib · Ubuntu 22.04 · Git

## Roadmap
- [x] Phase 1 — Python PID Simulation
- [ ] Phase 2 — ROS 2 Nodes
- [ ] Phase 3 — Gazebo 3D Simulation
- [ ] Phase 4 — Full Balancing Robot