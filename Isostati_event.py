import numpy as np
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt

class ATMIsostaticEngine:
    """
    ATM MULTIVERSE ENGINE - Integrated Monitoring
    Simulates 10,000 nodes across nested sub-lattices
    and tracks convergence, harmonic formation, and density structure.
    """
    def __init__(self, n_nodes=10000):
        # 1. INITIALIZE THE SUBSTRATE BULK (10,000 Nodes)
        self.pos = np.random.rand(n_nodes, 3)
        # Primary Isostatic Harmonics (Standard 1.52 variants)
        self.freqs = np.random.choice([50.0, 100.0], n_nodes) 
        self.lattice_phases = np.where(self.freqs == 50.0, 'Substrate', 'Rigid_Lattice')
        self.substrate_heat = np.zeros(n_nodes)
        self.h_z = 0.001 # Metric Expansion Factor

        # --- MONITORING ---
        self.res_history = []
        self.harmonic_count = []
        self.density_histograms = []

    def step(self, r_connect=0.08, k_elastic=0.02):
        # 2. SPATIAL PARTITIONING (Optimized for 10k nodes)
        tree = cKDTree(self.pos)
        pairs = np.array(list(tree.query_pairs(r_connect)))
        
        if len(pairs) > 0:
            i, j = pairs[:, 0], pairs[:, 1]
            diff = self.pos[j] - self.pos[i]
            dist = np.linalg.norm(diff, axis=1, keepdims=True) + 1e-7
            
            # 3. ISOSTATIC RESONANCE (The Pull)
            res = 1.0 - np.abs(self.freqs[i] - self.freqs[j]) / (self.freqs[i] + self.freqs[j])
            res = res.reshape(-1, 1)
            
            # 4. ENTROPY PRESSURE (The Push)
            temp_diff = (self.substrate_heat[j] - self.substrate_heat[i]).reshape(-1, 1)
            pressure_force = (diff / dist) * temp_diff * 0.05
            
            # 5. APPLY LATTICE FORCES
            forces = np.zeros_like(self.pos)
            pull_mask = (self.lattice_phases[i] == self.lattice_phases[j]) | (res.flatten() > 0.85)
            strength = k_elastic * res[pull_mask]
            f_pull = (diff[pull_mask] / dist[pull_mask]) * (dist[pull_mask] * strength)
            
            np.add.at(forces, i[pull_mask], f_pull)
            np.add.at(forces, j[pull_mask], -f_pull)
            np.add.at(forces, i, -pressure_force)
        else:
            forces = np.zeros_like(self.pos)
            res = np.array([0])
        
        # 6. METRIC EXPANSION & COOLING
        self.pos *= (1 + self.h_z)
        self.pos += forces
        self.substrate_heat *= 0.98

        # --- MONITORING ---
        self.res_history.append(res.mean())
        self.harmonic_count.append(np.sum(self.lattice_phases == 'Harmonic'))
        H, edges = np.histogramdd(self.pos, bins=(10,10,10))
        self.density_histograms.append(H.mean())

        return self.pos

    def trigger_isostatic_event(self):
        """Injects the 150Hz Alpha-Omega Harmonic."""
        tree = cKDTree(self.pos)
        pairs = np.array(list(tree.query_pairs(0.02)))
        
        for i, j in pairs:
            if self.lattice_phases[i] != self.lattice_phases[j]:
                self.substrate_heat[i] += 1.0
                if np.random.rand() > 0.95:
                    self.freqs[i] = 150.0
                    self.lattice_phases[i] = 'Harmonic'

# --- EXECUTE ENGINE ---
engine = ATMIsostaticEngine(10000)

print("Starting 10,000-node ATM Isostatic Engine with Monitoring...")
for frame in range(200):
    engine.step()
    engine.trigger_isostatic_event()
    
    if frame in [50, 100, 150, 199]:
        print(f"Frame {frame}: Avg Res={engine.res_history[-1]:.3f}, "
              f"Harmonic Nodes={engine.harmonic_count[-1]}, Avg Density={engine.density_histograms[-1]:.3f}")

# --- VISUALIZATION ---
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.plot(engine.res_history, color='cyan')
plt.title("1.52 Harmonic Convergence")
plt.xlabel("Frame")
plt.ylabel("Average Resonance")

plt.subplot(1,3,2)
plt.plot(engine.harmonic_count, color='magenta')
plt.title("Harmonic Node Formation")
plt.xlabel("Frame")
plt.ylabel("Nodes in Harmonic Phase")

plt.subplot(1,3,3)
plt.plot(engine.density_histograms, color='orange')
plt.title("Manifold Density (Voids & Filaments)")
plt.xlabel("Frame")
plt.ylabel("Mean Cell Density")

plt.tight_layout()
plt.show()

print("ATM Isostatic Manifold fully crystallized. Monitoring Complete. Ready for Archival.")
