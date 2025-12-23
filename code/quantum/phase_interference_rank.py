import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Problem setup
# -----------------------------

X_MIN, X_MAX = -6.0, 6.0
M = 128                  # number of discrete positions
N_SHOTS = 20000          # Monte Carlo measurements

np.random.seed(42)

# Twin-peaks deceptive fitness
def fitness_twin_peaks(x):
    return 10*np.exp(-(x-3)**2) + 5*np.exp(-(x+3)**2)

# Discretized domain
x_grid = np.linspace(X_MIN, X_MAX, M)
fitness = fitness_twin_peaks(x_grid)

# Basin definition
left_mask = x_grid < 0
right_mask = x_grid >= 0

# -----------------------------
# 2. Classical baseline
# -----------------------------

def classical_sampling():
    samples = np.random.choice(M, size=N_SHOTS)
    left = np.sum(left_mask[samples])
    right = np.sum(right_mask[samples])
    return left / N_SHOTS, right / N_SHOTS

# -----------------------------
# 3. Quantum utilities
# -----------------------------

def uniform_state(M):
    return np.ones(M, dtype=np.complex128) / np.sqrt(M)

def rank_phase_encoding(fitness):
    """
    Rank-based phase:
    phi_i = 2π * rank_i / M
    """
    ranks = np.argsort(np.argsort(fitness))
    phases = 2 * np.pi * ranks / M
    return np.exp(1j * phases)

def apply_dft(state):
    return np.fft.fft(state) / np.sqrt(len(state))

def measure_state(state):
    probs = np.abs(state)**2
    probs /= probs.sum()
    samples = np.random.choice(len(state), size=N_SHOTS, p=probs)
    left = np.sum(left_mask[samples])
    right = np.sum(right_mask[samples])
    return left / N_SHOTS, right / N_SHOTS

# -----------------------------
# 4. Experiments
# -----------------------------

# Classical
cl_left, cl_right = classical_sampling()

# Quantum: superposition only
psi0 = uniform_state(M)
sup_left, sup_right = measure_state(psi0)

# Quantum: rank-phase + interference
phase = rank_phase_encoding(fitness)
psi_rank = psi0 * phase
psi_rank_mixed = apply_dft(psi_rank)
rk_left, rk_right = measure_state(psi_rank_mixed)

# -----------------------------
# 5. Results
# -----------------------------

print("\n=== Basin Capture Probabilities ===\n")

print("Classical sampling:")
print(f"  Left basin  = {cl_left:.3f}")
print(f"  Right basin = {cl_right:.3f}\n")

print("Quantum (superposition only):")
print(f"  Left basin  = {sup_left:.3f}")
print(f"  Right basin = {sup_right:.3f}\n")

print("Quantum (rank-phase + interference):")
print(f"  Left basin  = {rk_left:.3f}")
print(f"  Right basin = {rk_right:.3f}")

# -----------------------------
# 6. Optional visualization
# -----------------------------

plt.figure(figsize=(6,4))
plt.plot(x_grid, fitness, label="Fitness landscape")
plt.axvline(0, color='k', linestyle='--', alpha=0.5)
plt.title("Twin Peaks Fitness Landscape")
plt.xlabel("x")
plt.ylabel("Fitness")
plt.legend()
plt.tight_layout()
plt.show()

