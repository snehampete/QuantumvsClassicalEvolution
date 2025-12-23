import numpy as np
import matplotlib.pyplot as plt

# Domain
X_MIN, X_MAX = -6.0, 6.0

# Twin peaks fitness (NOT used yet, just for visualization later)
def fitness_twin_peaks(x):
    return 10*np.exp(-(x-3)**2) + 5*np.exp(-(x+3)**2)

def classical_sampling(N):
    # Uniform iid samples
    xs = np.random.uniform(X_MIN, X_MAX, size=N)
    left = np.sum(xs < 0)
    right = np.sum(xs >= 0)
    return left, right

N = 10_000
cl_left, cl_right = classical_sampling(N)

print("Classical sampling:")
print("Left basin :", cl_left / N)
print("Right basin:", cl_right / N)

def make_grid(M):
    xs = np.linspace(X_MIN, X_MAX, M)
    return xs

M = 64
x_grid = make_grid(M)

def uniform_quantum_state(M):
    # |ψ> = (1/sqrt(M)) Σ |i>
    psi = np.ones(M, dtype=np.complex128) / np.sqrt(M)
    return psi

psi = uniform_quantum_state(M)
print("Norm:", np.sum(np.abs(psi)**2))


def quantum_measurements(psi, x_grid, N):
    probs = np.abs(psi)**2
    indices = np.random.choice(len(x_grid), size=N, p=probs)
    xs = x_grid[indices]
    left = np.sum(xs < 0)
    right = np.sum(xs >= 0)
    return left, right

q_left, q_right = quantum_measurements(psi, x_grid, N)

print("Quantum sampling:")
print("Left basin :", q_left / N)
print("Right basin:", q_right / N)


print("\nDifference (Quantum - Classical):")
print("Left basin :", (q_left - cl_left) / N)
print("Right basin:", (q_right - cl_right) / N)

Ms = [32, 64, 128, 256]

results = []

for M in Ms:
    x_grid = make_grid(M)
    psi = uniform_quantum_state(M)
    qL, qR = quantum_measurements(psi, x_grid, N)
    results.append((M, qL/N, qR/N))

for r in results:
    print(f"M={r[0]:3d} | Left={r[1]:.4f}, Right={r[2]:.4f}")


labels = [f"M={r[0]}" for r in results]
left_vals = [r[1] for r in results]
right_vals = [r[2] for r in results]

plt.figure()
plt.plot(labels, left_vals, label="Left basin")
plt.plot(labels, right_vals, label="Right basin")
plt.axhline(0.5, linestyle="--")
plt.ylabel("Probability")
plt.title("Quantum sampling vs resolution")
plt.legend()
plt.show()


# ============================================================
# EXPERIMENT 2: Phase-Structured Superposition (Interference)
# ============================================================


def phase_structured_state(x_grid, phi):
    M = len(x_grid)
    psi = np.zeros(M, dtype=np.complex128)
    for i, x in enumerate(x_grid):
        if x < 0:
            psi[i] = 1.0
        else:
            psi[i] = np.exp(1j * phi)
    psi /= np.linalg.norm(psi)
    return psi


def mix_state(psi):
    return np.fft.fft(psi) / np.sqrt(len(psi))


def measure_state(psi, x_grid, N):
    probs = np.abs(psi)**2
    idx = np.random.choice(len(x_grid), size=N, p=probs)
    xs = x_grid[idx]
    return np.sum(xs < 0), np.sum(xs >= 0)


M = 128
N = 10_000
phi = np.pi  # strong phase contrast

x_grid = np.linspace(-6, 6, M)

psi = phase_structured_state(x_grid, phi)
psi_mixed = mix_state(psi)

L, R = measure_state(psi_mixed, x_grid, N)

print("After phase + mixing:")
print("Left :", L/N)
print("Right:", R/N)


phis = [0, np.pi/4, np.pi/2, np.pi, 3*np.pi/2]
for phi in phis:
    psi = phase_structured_state(x_grid, phi)
    psi_mixed = mix_state(psi)
    L, R = measure_state(psi_mixed, x_grid, N)
    print(f"phi={phi:.2f} → Left={L/N:.3f}, Right={R/N:.3f}")

