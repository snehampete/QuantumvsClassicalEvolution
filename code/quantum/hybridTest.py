import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 1. Problem setup
# ===============================

X_MIN, X_MAX = -6.0, 6.0
POP = 200
M = 128          # discretization for quantum state
ELITISM = 10
TOURNAMENT_K = 5
np.random.seed(42)

def fitness_twin_peaks(x):
    return 10*np.exp(-(x-3)**2) + 5*np.exp(-(x+3)**2)

# ===============================
# 2. Classical selection
# ===============================

def tournament_selection(pop, fit, k, elitism):
    new_pop = []
    elite_idx = np.argsort(fit)[-elitism:]
    new_pop.extend(pop[elite_idx])

    while len(new_pop) < len(pop):
        idx = np.random.choice(len(pop), k, replace=False)
        winner = idx[np.argmax(fit[idx])]
        new_pop.append(pop[winner])

    return np.array(new_pop)

# ===============================
# 3. Quantum exploration step
# ===============================

def quantum_explore(population):
    # discretize domain
    x_grid = np.linspace(X_MIN, X_MAX, M)

    # encode population density as amplitudes
    hist, _ = np.histogram(population, bins=M, range=(X_MIN, X_MAX))
    psi = hist.astype(float)

    # if population collapses completely, avoid zero state
    if np.linalg.norm(psi) == 0:
        psi[:] = 1.0

    psi = psi / np.linalg.norm(psi)

    # coherent global mixing (DFT)
    psi_mixed = np.fft.fft(psi) / np.sqrt(M)

    # measurement probabilities
    probs = np.abs(psi_mixed)**2
    probs = probs / probs.sum()

    # resample population
    indices = np.random.choice(M, size=len(population), p=probs)
    new_population = x_grid[indices]

    return new_population

# ===============================
# 4. Collapse detection
# ===============================

def basin_occupancy(pop):
    left = np.mean(pop < 0)
    right = np.mean(pop >= 0)
    return left, right

def collapsed(pop, threshold=0.9):
    left, right = basin_occupancy(pop)
    return (left > threshold) or (right > threshold)

# ===============================
# 5. One-generation comparison
# ===============================

# initial population
population = np.random.uniform(X_MIN, X_MAX, size=POP)
fitness = fitness_twin_peaks(population)

print("Initial basin occupancy:", basin_occupancy(population))

# ----- Classical-only step -----
classical_selected = tournament_selection(
    population,
    fitness,
    TOURNAMENT_K,
    ELITISM
)

print("After classical selection:", basin_occupancy(classical_selected))

# ----- Hybrid step (collapse-triggered) -----
if collapsed(population):
    print("Collapse detected → applying quantum exploration")
    explored = quantum_explore(population)
else:
    explored = population.copy()

fitness_explored = fitness_twin_peaks(explored)
hybrid_selected = tournament_selection(
    explored,
    fitness_explored,
    TOURNAMENT_K,
    ELITISM
)

print("After hybrid step:", basin_occupancy(hybrid_selected))

# ===============================
# 6. Visualization
# ===============================

xs = np.linspace(X_MIN, X_MAX, 1000)
plt.figure(figsize=(10,4))
plt.plot(xs, fitness_twin_peaks(xs), label="Fitness landscape")

plt.scatter(classical_selected, fitness_twin_peaks(classical_selected),
            s=10, alpha=0.6, label="Classical")
plt.scatter(hybrid_selected, fitness_twin_peaks(hybrid_selected),
            s=10, alpha=0.6, label="Hybrid")

plt.legend()
plt.title("Classical vs Hybrid (one generation)")
plt.xlabel("x")
plt.ylabel("fitness")
plt.show()
