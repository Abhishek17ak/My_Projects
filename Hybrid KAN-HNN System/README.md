# Hybrid KAN-HNN Architecture for Conservative Dynamical Systems

## Overview
This project introduces a **Hybrid KAN-HNN Architecture**, a novel framework designed to model conservative dynamical systems while preserving physical principles like energy conservation and symplectic structure. The architecture combines **Kolmogorov-Arnold Networks (KANs)** for efficient function approximation using B-splines and **Hamiltonian Neural Networks (HNNs)** to enforce physics-informed constraints.

By integrating data-driven learning with first-principles physics, this hybrid model achieves long-term stability, interpretability, and computational efficiency, making it ideal for scientific simulations and engineering applications.

---

## Key Features
- **Kolmogorov-Arnold Networks (KAN):**
  - Utilizes B-spline-based activation functions for feature extraction and function approximation.
  - Provides interpretability through spline visualizations.
  
- **Hamiltonian Neural Networks (HNN):**
  - Encodes Hamiltonian mechanics to preserve energy conservation and symplectic structure.
  - Ensures physically consistent predictions without post-hoc regularization.

- **Applications:**
  - Orbital mechanics 🚀
  - Molecular dynamics 🧪
  - Robotics control systems 🤖
  - Climate modeling 🌍

---

## Results
The Hybrid KAN-HNN model was validated on benchmark systems:
1. **Simple Harmonic Oscillator**:
   - Achieved perfect circular phase space trajectories, maintaining energy conservation.
2. **Double Pendulum**:
   - Successfully modeled chaotic dynamics while preserving stability.

---

## Medium Article
Learn more about the story behind this research: [Read on Medium](https://medium.com/@abhishek.kalugade17/beyond-neural-networks-how-i-built-a-physics-inspired-ai-to-model-the-universe-8f59e0b7856b)


---

## Contact
Feel free to reach out for collaborations or discussions:
- **Author:** Abhishek Kalugade  
- **Email:** abhishek.kalugade@stonybrook.edu  
