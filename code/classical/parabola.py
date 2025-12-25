
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import trange
import json, os

# ----- Config -----
np.random.seed(34)
OUTDIR = "part1_results"
os.makedirs(OUTDIR, exist_ok=True)

# GA hyperparams (tweak later if needed)
POP_SIZE = 30
GENS = 80
ELITISM =2
TOURNAMENT_K = 5
CROSSOVER_PROB = 0.4
MUTATION_PM = 0.5
MUTATION_SIGMA = 1
TRIALS = 10
DOMAIN = (-5, 5)

# ----- Landscape (parabola) -----
def fitness_simple(x):
    return 10 - x**2

# ----- GA primitives (clean, reproducible) -----
def init_pop(N, domain):
    return np.random.uniform(domain[0], domain[1], size=N)

def evaluate(pop, fitness_fn):
    return fitness_fn(pop)

def tournament_select(pop, scores, k=3):
    N = pop.size
    parents = []
    for _ in range(N):
        idx = np.random.randint(0, N, size=k)
        winner = idx[np.argmax(scores[idx])]
        parents.append(pop[winner])
    return np.array(parents)

def blend_crossover(parents, pc=0.8):
    N = parents.size
    children = parents.copy()
    for i in range(0, N - 1, 2):
        if np.random.rand() < pc:
            a, b = parents[i], parents[i+1]
            alpha = np.random.rand()
            children[i]   = alpha*a + (1-alpha)*b
            children[i+1] = (1-alpha)*a + alpha*b
    return children

def mutate(children, pm=0.2, sigma=0.3, domain=None):
    mask = np.random.rand(children.size) < pm
    children[mask] += np.random.normal(0, sigma, size=mask.sum())
    if domain is not None:
        children = np.clip(children, domain[0], domain[1])
    return children

def run_single_ga(fitness_fn, domain, seed=None, record_positions=True):
    if seed is not None:
        np.random.seed(seed)
    pop = init_pop(POP_SIZE, domain)
    best_hist = []
    mean_hist = []
    std_hist = []
    positions = [] if record_positions else None

    for gen in range(GENS):
        scores = evaluate(pop, fitness_fn)
        best_hist.append(scores.max())
        mean_hist.append(scores.mean())
        std_hist.append(scores.std())
        if record_positions:
            positions.append(pop.copy())

        # elitism
        elites_idx = np.argsort(scores)[-ELITISM:]
        elites = pop[elites_idx]

        # selection/crossover/mutation
        parents = tournament_select(pop, scores, k=TOURNAMENT_K)
        children = blend_crossover(parents, pc=CROSSOVER_PROB)
        children = mutate(children, pm=MUTATION_PM, sigma=MUTATION_SIGMA, domain=domain)

        # choose best children to fill population (keeps improvement pressure)
        child_scores = evaluate(children, fitness_fn)
        best_children_idx = np.argsort(child_scores)[- (POP_SIZE - ELITISM):]
        pop = np.concatenate([elites, children[best_children_idx]])

    return {
        "best": np.array(best_hist),
        "mean": np.array(mean_hist),
        "std": np.array(std_hist),
        "positions": positions
    }

# ----- Run TRIALS and compute metrics -----
def run_trials_parabola(trials=10):
    xs = np.linspace(DOMAIN[0], DOMAIN[1], 2001)
    fs = fitness_simple(xs)
    global_max = fs.max()
    success_thresh = global_max - 1e-6

    runs = []
    success = 0
    for t in trange(trials, desc="Parabola trials"):
        seed = 1000 + t
        res = run_single_ga(fitness_simple, DOMAIN, seed=seed, record_positions=True)
        runs.append(res)
        if res["best"][-1] >= success_thresh:
            success += 1

    summary = {
        "global_max": float(global_max),
        "success_rate": success / trials,
        "trials": trials
    }
    return {"runs": runs, "summary": summary, "xs": xs.tolist(), "fs": fs.tolist()}

results = run_trials_parabola(TRIALS)

# ----- Save numeric summary -----
with open(os.path.join(OUTDIR, "parabola_summary.json"), "w") as f:
    json.dump(results["summary"], f, indent=2)

# ----- Plot aggregated metrics -----
def plot_aggregate(runs, title):
    G = runs[0]["best"].size
    best_matrix = np.array([r["best"] for r in runs])
    median = np.median(best_matrix, axis=0)
    q1 = np.percentile(best_matrix, 25, axis=0)
    q3 = np.percentile(best_matrix, 75, axis=0)

    plt.fill_between(range(G), q1, q3, alpha=0.2)
    plt.plot(range(G), median, label="median best")
    plt.xlabel("Generation"); plt.ylabel("Best fitness"); plt.title(title)
    plt.grid(True); plt.legend()
    plt.savefig(os.path.join(OUTDIR, "parabola_aggregate.png"))
    plt.show()

plot_aggregate(results["runs"], "Parabola: Best Fitness (median over trials)")

# ----- Animation for the first trial -----
def make_animation_one_run(run, xs, fs, filename):
    positions = run["positions"]
    G = len(positions)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(xs, fs, '-k', lw=1)
    ax.set_xlim(DOMAIN[0], DOMAIN[1])
    ax.set_xlabel("x"); ax.set_ylabel("Fitness")
    scat = ax.scatter(positions[0], fitness_simple(np.array(positions[0])), s=40, c='red')

    def update(i):
        pts = positions[i]
        scat.set_offsets(np.vstack([pts, fitness_simple(np.array(pts))]).T)
        ax.set_title(f"Gen {i}")
        return scat,

    anim = animation.FuncAnimation(fig, update, frames=G, interval=150, blit=True)
    anim.save(filename, writer='ffmpeg', dpi=150)
    plt.close(fig)

# Save animation for run 0
anim_fn = os.path.join(OUTDIR, "parabola_run0.mp4")
make_animation_one_run(results["runs"][0], np.array(results["xs"]), np.array(results["fs"]), anim_fn)

# ----- Print concise report -----
print("Parabola summary:", results["summary"])
print("Saved: ", os.path.join(OUTDIR, "parabola_aggregate.png"))
print("Saved animation (run 0):", anim_fn)

