# ===================== IMPORTS =====================
import numpy as np
import json
import os
import pickle
import matplotlib.pyplot as plt
from matplotlib import animation

# ===================== RASTRIGIN 2D =====================
A = 10.0

def rastrigin_2d(X):
    """
    X: (N, 2)
    returns: (N,)
    Global optimum at (0,0) with fitness = 2A
    """
    x = X[:, 0]
    y = X[:, 1]
    return 2*A - ((x**2 - A*np.cos(2*np.pi*x)) +
                  (y**2 - A*np.cos(2*np.pi*y)))

# ===================== CLASSICAL GA =====================
def run_ga_rastrigin_2d(
    pop_size=40,
    gens=150,
    elitism=2,
    crossover_prob=0.8,
    mutation_prob=0.2,
    mutation_sigma=0.3,
    domain=(-5.12, 5.12),
    seed=None
):
    if seed is not None:
        np.random.seed(seed)

    pop = np.random.uniform(domain[0], domain[1], size=(pop_size, 2))

    best_fitness = []
    best_dist = []
    diversity = []
    pop_history = []

    for g in range(gens):
        fitness = rastrigin_2d(pop)
        pop_history.append(pop.copy())

        idx = np.argmax(fitness)
        best_fitness.append(fitness[idx])
        best_dist.append(np.linalg.norm(pop[idx]))
        diversity.append(np.mean(np.std(pop, axis=0)))

        elite_idx = np.argsort(fitness)[-elitism:]
        elites = pop[elite_idx]
        new_pop = [e.copy() for e in elites]

        def tournament():
            k = 3
            idxs = np.random.choice(pop_size, k, replace=False)
            return pop[idxs[np.argmax(fitness[idxs])]]

        while len(new_pop) < pop_size:
            p1, p2 = tournament(), tournament()

            if np.random.rand() < crossover_prob:
                alpha = np.random.rand()
                child = alpha*p1 + (1-alpha)*p2
            else:
                child = p1.copy()

            if np.random.rand() < mutation_prob:
                child += np.random.normal(0, mutation_sigma, size=2)

            child = np.clip(child, domain[0], domain[1])
            new_pop.append(child)

        pop = np.array(new_pop)

    return {
        "best_fitness": np.array(best_fitness),
        "best_distance": np.array(best_dist),
        "diversity": np.array(diversity),
        "pop_history": pop_history
    }

# ===================== RUN EXPERIMENTS =====================
TRIALS = 30
results = []

for s in range(TRIALS):
    results.append(run_ga_rastrigin_2d(seed=s))

final_distances = [r["best_distance"][-1] for r in results]

print("median final distance:", np.median(final_distances))
print("std final distance:", np.std(final_distances))

# ===================== PLOTS =====================
plt.figure(figsize=(7,4))
for r in results:
    plt.plot(r["best_fitness"], alpha=0.5)
plt.xlabel("Generation")
plt.ylabel("Best fitness")
plt.title("2D Rastrigin – Best Fitness vs Generation")
plt.show()

plt.figure(figsize=(7,4))
for r in results:
    plt.plot(r["best_distance"], alpha=0.5)
plt.yscale("log")
plt.xlabel("Generation")
plt.ylabel("Distance to (0,0)")
plt.title("2D Rastrigin – Distance to Global Optimum")
plt.show()

plt.figure(figsize=(7,4))
for r in results:
    plt.plot(r["diversity"], alpha=0.5)
plt.xlabel("Generation")
plt.ylabel("Population diversity")
plt.title("2D Rastrigin – Diversity vs Generation")
plt.show()

# ===================== SAVE RESULTS =====================
os.makedirs("results", exist_ok=True)

summary = {
    "final_distances": final_distances,
    "median_final_distance": float(np.median(final_distances)),
    "std_final_distance": float(np.std(final_distances)),
    "params": {
        "pop_size": 40,
        "gens": 150,
        "elitism": 2,
        "mutation_sigma": 0.3,
        "mutation_prob": 0.2
    }
}

with open("results/rastrigin_2d_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

with open("results/rastrigin_2d_full_runs.pkl", "wb") as f:
    pickle.dump(results, f)

# ===================== ANIMATION =====================
x = np.linspace(-5.12, 5.12, 300)
y = np.linspace(-5.12, 5.12, 300)
X, Y = np.meshgrid(x, y)
Z = 2*A - ((X**2 - A*np.cos(2*np.pi*X)) +
           (Y**2 - A*np.cos(2*np.pi*Y)))

run = results[0]
pop_hist = run["pop_history"]

fig, ax = plt.subplots(figsize=(6,6))
ax.contourf(X, Y, Z, levels=50, cmap="viridis")
scat = ax.scatter([], [], c="red", s=20)

ax.set_xlim(-5.12, 5.12)
ax.set_ylim(-5.12, 5.12)

def update(frame):
    scat.set_offsets(pop_hist[frame])
    ax.set_title(f"Generation {frame}")
    return scat,

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(pop_hist),
    interval=150
)

ani.save("results/rastrigin_2d_ga.mp4", writer="ffmpeg", dpi=150)

