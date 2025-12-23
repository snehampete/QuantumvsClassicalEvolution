Classical evolutionary algorithms are analyzed first to establish a clear, well-understood baseline of how population-based stochastic search behaves on different fitness landscapes. The purpose of this analysis is not to claim novelty or improved performance, but to explicitly identify *where and why* standard evolutionary dynamics succeed, converge prematurely, or become trapped in local optima under known conditions. By characterizing these failure modes through controlled landscapes and measurable diagnostics, this section provides the necessary reference point against which any later modifications or alternative mechanisms can be meaningfully compared.

## 1.1 Parabolic landscape — success case

### Fitness function

We begin with a simple one-dimensional convex fitness landscape defined as

[
f(x) = 10 - x^2, x belonging to [-5,5]
]

This landscape has a **single global maximum** at (x = 0), no local optima, and a smooth, monotonic gradient toward the peak from any initial position.

---

### Visualization and plots

1. **Fitness curve** (parabola): shows the global structure of the landscape and the location of the unique optimum.
2. **Population evolution plot / animation**: shows individuals initially scattered across the domain and progressively collapsing toward (x=0).

---

### Observed GA behavior

Across multiple independent trials, the classical genetic algorithm consistently converges to the global maximum. The population’s best fitness rapidly increases in early generations, while population diversity (standard deviation) decreases as individuals cluster around the optimum. The final population collapses tightly near (x=0).

This behavior is stable across reasonable choices of mutation rate, crossover probability, and selection pressure.

---

### Why this landscape is easy

This landscape is easy for classical evolution because:

* **No local optima**: there are no deceptive traps or competing basins.
* **Convexity**: any small perturbation toward the center improves fitness.
* **Smooth gradients**: mutation and crossover almost always generate offspring closer to the optimum once the population is near it.
* **Selection alignment**: fitness ranking directly corresponds to distance from the global optimum.

As a result, even weak mutation and moderate selection pressure are sufficient for reliable convergence.

---

### What “success” means in this context

Success is defined as:

* The best individual in the population reaching fitness arbitrarily close to the known global maximum (f(0) = 10), and
* This occurring consistently across independent runs (high success rate).

Because the global optimum is known analytically, success can be unambiguously measured.

---

### Why this case is included

This case is included **not to demonstrate algorithmic novelty**, but to establish a **baseline sanity check**:

* It verifies that the genetic algorithm is implemented correctly.
* It confirms that selection, crossover, mutation, and elitism behave as expected on a well-behaved landscape.
* It ensures that any failures observed later on more complex landscapes are due to **landscape structure**, not coding errors or pathological parameter choices.

---

### Why convergence here is expected—and uninformative for exploration

Convergence on a convex parabola is **guaranteed** for classical evolutionary algorithms under minimal assumptions. There are no fitness barriers, no competing basins, and no requirement for long-range exploration.

Therefore, while this case demonstrates that the GA “works,” it provides **no insight into escape mechanisms, exploration limits, or the potential advantages of quantum dynamics**. Any algorithm capable of hill-climbing will succeed here.

For this reason, the parabolic landscape serves strictly as a **control experiment**, establishing expected success before moving to deceptive and multimodal landscapes where classical evolution can fail.

---

**Conclusion:**
The plots produced by our code are sufficient for this section. Further analysis on this landscape would be redundant and does not inform the central research question of when (and why) quantum evolution might outperform classical evolution.
