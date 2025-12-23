
# classical_deceptive_research_with_anim.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import trange
import os, json

# ============================================================
# 1. FROZEN PARAMETERS (DO NOT TUNE)
# ============================================================
POP = 30
GENS = 80
ELITISM = 2
TOURNAMENT_K = 5
MUT_P = 0.2
MUT_SIGMA = 0.15
DOMAIN = (-8, 8)
TRIALS = 40

np.random.seed(42)

OUTDIR = "classical_deceptive_results"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# 2. STRONGLY DECEPTIVE LANDSCAPE (FINAL)
# ============================================================
def fitness(x):
    return (
        8 * np.exp(-(x + 4)**2 / 1.5)    # wide local trap
        + 10 * np.exp(-(x - 2)**2 / 0.2) # narrow global optimum
    )

# ============================================================
# 3. GA PRIMITIVES
# ============================================================
def init_pop():
    return np.random.uniform(DOMAIN[0], DOMAIN[1], POP)

def tournament_select(pop, scores):
    parents = []
    for _ in range(POP):
        idx = np.random.randint(0, POP, TOURNAMENT_K)
        parents.append(pop[idx[np.argmax(scores[idx])]])
    return np.array(parents)

def blend_crossover(parents):
    children = parents.copy()
    for i in range(0, POP-1, 2):
        a, b = parents[i], parents[i+1]
        alpha = np.random.rand()
        children[i]   = alpha*a + (1-alpha)*b
        children[i+1] = (1-alpha)*a + alpha*b
    return children

def mutate(children):
    mask = np.random.rand(POP) < MUT_P
    children[mask] += np.random.normal(0, MUT_SIGMA, mask.sum())
    return np.clip(children, DOMAIN[0], DOMAIN[1])

# ============================================================
# 4. SINGLE RUN (RECORD EVERYTHING, INCLUDING POPS)
# ============================================================
def run_single(seed):
    np.random.seed(seed)
    pop = init_pop()

    best_hist = []
    std_hist = []
    pop_hist = []          # <- NEW: store population each generation

    for g in range(GENS):
        scores = fitness(pop)
        best_hist.append(scores.max())
        std_hist.append(pop.std())
        pop_hist.append(pop.copy())

        elites = pop[np.argsort(scores)[-ELITISM:]]
        parents = tournament_select(pop, scores)
        children = blend_crossover(parents)
        children = mutate(children)

        child_scores = fitness(children)
        best_children = children[np.argsort(child_scores)[-(POP-ELITISM):]]

        pop = np.concatenate([elites, best_children])

    final_pop = pop.copy()
    return {
        "best_fitness": best_hist[-1],
        "best_hist": best_hist,
        "std_hist": std_hist,
        "final_pop": final_pop,
        "pop_hist": pop_hist      # <- NEW
    }

# ============================================================
# 5. PEAK DETECTION (ROBUST)
# ============================================================
xs_dense = np.linspace(DOMAIN[0], DOMAIN[1], 5000)
fs_dense = fitness(xs_dense)

global_x = xs_dense[np.argmax(fs_dense)]
mask = np.abs(xs_dense - global_x) > 1.0
local_x = xs_dense[mask][np.argmax(fs_dense[mask])]

def classify_run(final_pop):
    best_x = final_pop[np.argmax(fitness(final_pop))]
    if abs(best_x - global_x) < 0.5:
        return "global"
    elif abs(best_x - local_x) < 0.5:
        return "local"
    else:
        return "other"

# ============================================================
# 6. RUN EXPERIMENTS
# ============================================================
runs = []
stats = {"global": 0, "local": 0, "other": 0}

for t in trange(TRIALS, desc="Running deceptive GA trials"):
    res = run_single(seed=1000 + t)
    label = classify_run(res["final_pop"])
    stats[label] += 1
    runs.append(res)

# ============================================================
# 7. SAVE SUMMARY
# ============================================================
summary = {
    "params": {
        "POP": POP,
        "GENS": GENS,
        "ELITISM": ELITISM,
        "TOURNAMENT_K": TOURNAMENT_K,
        "MUT_P": MUT_P,
        "MUT_SIGMA": MUT_SIGMA
    },
    "results": stats,
    "trials": TRIALS,
    "global_peak_x": float(global_x),
    "local_peak_x": float(local_x)
}

with open(os.path.join(OUTDIR, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("\nSUMMARY:", summary)

# ============================================================
# 8. AGGREGATE PLOTS (SANITY CHECK)
# ============================================================
best_matrix = np.array([r["best_hist"] for r in runs])
median = np.median(best_matrix, axis=0)
q1 = np.percentile(best_matrix, 25, axis=0)
q3 = np.percentile(best_matrix, 75, axis=0)

plt.figure(figsize=(7,4))
plt.fill_between(range(GENS), q1, q3, alpha=0.3, label="IQR")
plt.plot(median, label="Median best fitness")
plt.xlabel("Generation")
plt.ylabel("Best fitness")
plt.title("Classical GA on Deceptive Landscape")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(OUTDIR, "aggregate_best_fitness.png"))
plt.show()

# ============================================================
# 9. ANIMATION OF POPULATION EVOLUTION
# ============================================================
# choose one run to animate (e.g. first)
run_to_anim = runs[0]
pop_hist = run_to_anim["pop_hist"]

fig, ax = plt.subplots(figsize=(7,4))
ax.plot(xs_dense, fs_dense, 'k-', lw=1)       # fitness landscape
ax.set_xlim(DOMAIN)
ax.set_ylim(0, fs_dense.max() * 1.1)
ax.set_xlabel("x")
ax.set_ylabel("fitness")
ax.set_title("GA population over generations")

# initial scatter: positions vs fitness(x)
scat = ax.scatter(pop_hist[0], fitness(np.array(pop_hist[0])),
                  c='tab:blue', s=30, alpha=0.7)

gen_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

def init():
    scat.set_offsets(np.c_[pop_hist[0], fitness(np.array(pop_hist[0]))])
    gen_text.set_text("Generation 0")
    return scat, gen_text

def update(frame):
    x = np.array(pop_hist[frame])
    y = fitness(x)
    scat.set_offsets(np.c_[x, y])
    gen_text.set_text(f"Generation {frame}")
    return scat, gen_text

anim = animation.FuncAnimation(
    fig, update, init_func=init,
    frames=len(pop_hist), interval=150, blit=True
)

# save as mp4 (requires ffmpeg installed) and also show
mp4_path = os.path.join(OUTDIR, "deceptive_evolution.mp4")
writer = animation.FFMpegWriter(fps=10)
anim.save(mp4_path, writer=writer)
plt.show()


