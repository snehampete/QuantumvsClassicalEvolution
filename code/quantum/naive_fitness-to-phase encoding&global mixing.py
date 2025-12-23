
import numpy as np
import matplotlib.pyplot as plt

X_MIN, X_MAX = -6.0, 6.0

def fitness(x):
    return 10*np.exp(-(x-3)**2) + 5*np.exp(-(x+3)**2)

M = 256
x_grid = np.linspace(X_MIN, X_MAX, M)
f_vals = fitness(x_grid)


def classical_sampling(N):
    xs = np.random.uniform(X_MIN, X_MAX, size=N)
    left = np.sum(xs < 0)
    right = np.sum(xs >= 0)
    return left/N, right/N

def fitness_phase_state(x_grid, f_vals, alpha):
    psi = np.exp(1j * alpha * f_vals)
    psi = psi / np.linalg.norm(psi)
    return psi

def mix_state(psi):
    return np.fft.fft(psi) / np.sqrt(len(psi))


def measure_state(psi, x_grid, N):
    probs = np.abs(psi)**2
    idx = np.random.choice(len(x_grid), size=N, p=probs)
    xs = x_grid[idx]
    left = np.sum(xs < 0)
    right = np.sum(xs >= 0)
    return left/N, right/N

N = 20_000
alphas = [0.0, 0.05, 0.1, 0.2, 0.4]

print("Classical baseline:", classical_sampling(N))

for alpha in alphas:
    psi = fitness_phase_state(x_grid, f_vals, alpha)
    psi_mixed = mix_state(psi)
    L, R = measure_state(psi_mixed, x_grid, N)
    print(f"alpha={alpha:.2f} → Left={L:.3f}, Right={R:.3f}")
