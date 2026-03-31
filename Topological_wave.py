import numpy as np
import matplotlib.pyplot as plt

# --- ATM PARAMETERS ---
beta = 1.52          # Lattice stability constant
z_c = 5.85           # Yield / redshift threshold
f_epsilon = 150.0    # Hz, Epsilon Soul frequency
T_u = 0.3949         # Unit tension
Q_L = 1.2991         # Lattice heat
L_u = 5.39e-44       # Planck time in seconds

# --- SIMULATION SETTINGS ---
time_steps = 200
dt = L_u * 1e42      # Scaled time step for visualization
strain_history = []

# --- SIMULATE ISOSTATIC ΔR RIPPLE ---
for t in range(time_steps):
    # Time in seconds scaled to lattice dynamics
    t_sec = t * dt
    
    # Orbital-like inspiral of Epsilon nodes
    chirp_amp = T_u * (t / time_steps) * (1 + beta / z_c)
    
    # Phase oscillation using Epsilon frequency
    lattice_strain = chirp_amp * np.sin(2 * np.pi * f_epsilon * t_sec) 
    
    # Background tension floor from 1.52 harmonic
    lattice_strain += beta * T_u / Q_L
    
    strain_history.append(lattice_strain)

# --- PLOTTING ---
plt.figure(figsize=(10, 4))
plt.plot(strain_history, color='cyan', linewidth=2, label="ATM ΔR Ripple (1.52 Lattice)")
plt.title("ATM Topological Waveform: Isostatic ΔR Ripple")
plt.xlabel("Time Step (Scaled Substrate Clock)")
plt.ylabel("ΔR (Lattice Ripple Amplitude)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

print("Topological Waveform extracted. Fully ATM-parameter consistent with β=1.52, f_ε=150Hz.")
