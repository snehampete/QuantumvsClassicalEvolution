import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import trange
import os, json

# ================= CONFIG =================
np.random.seed(34)

OUTDIR = "part3_results"
os.makedirs(OUTDIR, exist_ok=True)

POP_SIZE = 40
GENS = 120
ELITISM = 2
TOURNAMENT_K = 3
CROSSOVER_PROB = 0.8
MUTATION_PM = 0.2
MUTATION_SIGMA = 0.35
TRIALS = 10
DOMAIN = (-5.12, 5.12)   # Standard Rastrigin domain
A = 10

# ================= LANDSCAPE =================
def rastrigin_1d_dense(x, k=4, A=10.0):
    """
    k = ripple frequency multiplier
    Higher k → more local optima per unit length
    """
    return A - (x**2 - A * np.cos(2 * np.pi * k * x))


# ================= GA PRIMITIVES =================
def init_population(N, domain):
    return np.random.uniform(domain[0], domain[1], size=N)

def evaluate(pop):
    return rastrigin_1d_dense(pop)

def tournament_selection(pop, scores, k):
    N = len(pop)
    parents = []
    for _ in range(N):
        idx = np.random.choice(N, k, replace=False)
        parents.append(pop[idx[np.argmax(scores[idx])]])
    return np.array(parents)

def blend_crossover(parents, pc):
    children = parents.copy()
    for i in range(0, len(parents)-1, 2):
        if np.random.rand() < pc:
            a, b = parents[i], parents[i+1]
            alpha = np.random.rand()
            children[i]   = alpha*a + (1-alpha)*b
            children[i+1] = (1-alpha)*a + alpha*b
    return children

def mutate(children, pm, sigma, domain):
    mask = np.random.rand(len(children)) < pm
    children[mask] += np.random.normal(0, sigma, size=mask.sum())
    return np.clip(children, domain[0], domain[1])

# ================= SINGLE RUN =================
def run_ga(seed=None, record_positions=True):
    if seed is not None:
        np.random.seed(seed)

    pop = init_population(POP_SIZE, DOMAIN)

    best_hist = []
    mean_hist = []
    std_hist  = []
    dist_hist = []
    positions = [] if record_positions else None

    for gen in range(GENS):
        scores = evaluate(pop)

        best_idx = np.argmax(scores)
        best_x = pop[best_idx]

        best_hist.append(scores[best_idx])
        mean_hist.append(scores.mean())
        std_hist.append(pop.std())
        dist_hist.append(abs(best_x - 0.0))

        if record_positions:
            positions.append(pop.copy())

        # ---- elitism ----
        elite_idx = np.argsort(scores)[-ELITISM:]
        elites = pop[elite_idx]

        # ---- evolution ----
        parents = tournament_selection(pop, scores, TOURNAMENT_K)
        children = blend_crossover(parents, CROSSOVER_PROB)
        children = mutate(children, MUTATION_PM, MUTATION_SIGMA, DOMAIN)

        child_scores = evaluate(children)
        best_children_idx = np.argsort(child_scores)[-(POP_SIZE - ELITISM):]

        pop = np.concatenate([elites, children[best_children_idx]])

    return {
        "best": np.array(best_hist),
        "mean": np.array(mean_hist),
        "std":  np.array(std_hist),
        "dist": np.array(dist_hist),
        "positions": positions
    }

# ================= MULTI-TRIAL RUN =================
runs = []
for t in trange(TRIALS, desc="Rastrigin trials"):
    runs.append(run_ga(seed=1000+t))

# ================= AGGREGATE PLOTS =================
def plot_with_iqr(data, ylabel, title, fname):
    mat = np.array(data)
    median = np.median(mat, axis=0)
    q1 = np.percentile(mat, 25, axis=0)
    q3 = np.percentile(mat, 75, axis=0)

    plt.fill_between(range(len(median)), q1, q3, alpha=0.2)
    plt.plot(median)
    plt.xlabel("Generation")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(os.path.join(OUTDIR, fname))
    plt.show()

plot_with_iqr([r["best"] for r in runs],
              "Best fitness",
              "Rastrigin: Best Fitness Over Time",
              "rastrigin_best.png")

plot_with_iqr([r["dist"] for r in runs],
              "Distance to global optimum |x−0|",
              "Rastrigin: Distance to Optimum",
              "rastrigin_distance.png")

plot_with_iqr([r["std"] for r in runs],
              "Population diversity (std)",
              "Rastrigin: Population Diversity",
              "rastrigin_diversity.png")

# ================= ANIMATION (ONE RUN) =================
xs = np.linspace(DOMAIN[0], DOMAIN[1], 3000)
fs = rastrigin_1d_dense(xs)

def animate_run(run, fname):
    fig, ax = plt.subplots(figsize=(9,4))
    ax.plot(xs, fs, 'k', lw=1)
    ax.scatter([0], [rastrigin_1d_dense(0)], c='green', s=80, label='Global Optimum')
    ax.set_xlim(DOMAIN)
    ax.set_xlabel("x")
    ax.set_ylabel("Fitness")
    ax.legend()

    scat = ax.scatter(run["positions"][0],
                      rastrigin_1d_dense(np.array(run["positions"][0])),
                      c='red', s=40)

    def update(i):
        pts = run["positions"][i]
        scat.set_offsets(np.c_[pts, rastrigin_1d_dense(pts)])
        ax.set_title(f"Generation {i}")
        return scat,

    anim = animation.FuncAnimation(fig, update, frames=GENS, interval=120)
    anim.save(fname, writer="ffmpeg", dpi=150)
    plt.close(fig)

anim_path = os.path.join(OUTDIR, "rastrigin_run0.mp4")
animate_run(runs[0], anim_path)

# ================= SUMMARY =================
summary = {
    "final_best_median": float(np.median([r["best"][-1] for r in runs])),
    "final_distance_median": float(np.median([r["dist"][-1] for r in runs]))
}

with open(os.path.join(OUTDIR, "rastrigin_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("Rastrigin summary:", summary)
print("Saved plots and animation to:", OUTDIR)

