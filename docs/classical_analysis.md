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

https://github.com/user-attachments/assets/393802f1-b374-4892-b2f6-b1a836300b28




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

## 1.2 Twin-Peaks Landscape — Deceptive Basin Capture

### Definition of the deceptive twin-peaks landscape

We consider a one-dimensional fitness landscape with two separated optima:

This landscape is deliberately **asymmetric**:

* The **global optimum** is the **narrow, high peak** near (x \approx 2).
* The **deceptive peak** is the **wider, lower peak** near (x \approx -4).

Although the global peak has higher fitness, the deceptive peak occupies a much larger region of the search space and therefore captures more individuals during early random sampling.

https://github.com/user-attachments/assets/bb507f54-36e2-470f-9ed5-b5144c7e3a4c



https://github.com/user-attachments/assets/6c52ce8d-5325-4b7d-922c-c1f7ac70b8e8



---

### Why this landscape is deceptive

The deception arises not from multiple optima alone, but from **basin geometry**:

* The deceptive basin is **wide and strongly attractive** under local selection.
* The global basin is **narrow and easy to miss**.
* The valley between them is low-fitness and steep.

As a result, early evolutionary dynamics are dominated by **basin volume**, not by absolute peak height.

---

### Observed classical GA behavior

Under fixed parameters, repeated runs of the same classical GA produce **different final outcomes**:

* Some runs converge to the global optimum.
* Other runs irreversibly collapse into the deceptive basin.

This behavior is **probabilistic**, not deterministic.(RNG etc is what decides this)
The same algorithm, parameters, and landscape can either succeed or fail depending only on early stochastic fluctuations.

---

### Premature convergence and basin capture

**Premature convergence** occurs when selection pressure causes the population to rapidly lose diversity before sufficient exploration has occurred.

In this landscape:

1. Early generations contain individuals in both basins due to random initialization.
2. The **wider deceptive basin** initially contains more moderately fit individuals.
3. Tournament selection preferentially amplifies these individuals.
4. Population variance collapses.
5. Once variance is low, the population becomes **dynamically trapped** inside the deceptive basin.

This process is called **basin capture**:
the population commits to a region of the landscape before discovering the true global structure.

---

### Why selection reinforces the wrong basin

Selection operates on **relative fitness within the current population**, not on global information.

If most individuals lie in the deceptive basin:

* Selection compares individuals **only within that basin**.
* The global peak contributes little or no signal once it is under-sampled.
* Selection therefore **amplifies the wrong basin**, even though it is globally inferior.

This is not a bug in selection—it is a fundamental limitation of local, population-based optimization.

---

### Why mutation and crossover do not reliably fix the failure

Once basin capture occurs:

* **Mutation**:

  * Small Gaussian mutations rarely produce jumps large enough to cross the low-fitness valley.
  * Large mutations destroy accumulated fitness and are eliminated by selection.
* **Crossover**:

  * Operates only on existing genetic material.
  * When all parents lie in the same basin, crossover cannot generate offspring outside it.

Thus, variation operators cannot overcome the trap **after diversity has collapsed**.

The failure is therefore **irreversible**, not just slow.

---

### Probabilistic failure, not deterministic failure

Crucially, classical evolution does not always fail here.

Instead:

* Failure probability is **non-zero and irreducible**.
* Early random fluctuations determine which basin captures the population.
* No fixed parameter setting guarantees success without sacrificing exploitation.

This distinguishes deceptive landscapes from trivial hard problems.

---

## Final sentence to anchor this section on deceptive landscapes

 *Classical genetic algorithms fail on deceptive twin-peaks landscapes not because they lack optimization power, but because early selection amplifies misleading basin structure, causing irreversible commitment under incomplete information.*

 ---

## 1.3 Rastrigin — Ruggedness × Dimensionality

### Definition (what landscape we are testing)

The Rastrigin function is a standard benchmark for rugged optimization. In (d) dimensions:

<img width="399" height="107" alt="image" src="https://github.com/user-attachments/assets/a6791407-d1f0-4e4c-8bdc-084cb9dafbb4" />

* Global optimum at x=0
* Fitness surface = smooth quadratic envelope + periodic oscillations
* Every dimension contributes **independent local optima**

This makes it ideal for isolating **ruggedness** from **deception**.

---

### Why Rastrigin is rugged 

* The cosine term introduces **regularly spaced local maxima and minima**
* Gradients are locally misleading but not globally inverted
* There is no “wrong basin” — the global optimum is visible in principle
* Difficulty arises because **local improvement signals decorrelate from global progress**

Ruggedness here means:

 many shallow traps that must be escaped **sequentially**.

---

### Why local optima explode with dimensionality

This is the critical scaling argument.

* In 1D:
  Number of local optima grows linearly with domain length.

* In 2D:
  Local optima form a **grid**.
  Count grows roughly as:
 (ripples per axis)^2

* In (d) dimensions:
  Local optima scale exponentially:
  O(k^d)
Each dimension multiplies the number of simultaneous traps.

This is **combinatorial ruggedness**, not just “more bumps.”

---

### What the 1D results show

**Observed behavior (from my runs):**

* Population reaches the global basin reliably
* Best solution converges to (x \approx 0) across runs
* Remaining motion is local oscillation near the optimum

**Interpretation:**

* Escaping individual barriers is easy
* Ruggedness alone does **not** defeat classical evolution at low dimension
* Randomness affects trajectories, not outcomes

This establishes a **baseline success regime**.

---

### What the 2D results show (the real failure)

**Observed behavior :**

* Median final distance (approximately 1), not near zero
* Large run-to-run variance
* Population clusters near the global basin but does not converge
* Long plateaus in fitness and distance curves

**Interpretation:**

* Progress requires **simultaneous escape** in multiple coordinates
* Escape probabilities multiply → become small
* Evolution remains active but inefficient

This is **convergence failure by dilution**, not trapping.

---

### Dilution of search 

As dimension increases:

* Population spreads over exponentially many local configurations
* Selection pressure is diluted across many near-equivalent solutions
* Mutation fixes one coordinate while breaking another
* Net global progress approaches zero

Formally:

 Finite population size cannot maintain coverage over an exponentially growing search space.

This is why simply increasing population size stops helping.

---

### Why population size does NOT save us

Empirically and conceptually:

* Doubling population gives linear sampling gain
* Landscape complexity grows exponentially
* Signal-to-noise ratio in selection collapses
* More individuals ≠ coordinated multi-dimensional progress

This is why classical GA scaling fails even without deception.

---


https://github.com/user-attachments/assets/0215138e-05fb-47e0-bfda-d8db5999e49b



https://github.com/user-attachments/assets/b57fbf8a-1f3d-4a92-9f73-8f03c2c2fab9



---
### One-sentence summary on rastrigin landscapes

 On Rastrigin landscapes, classical genetic algorithms fail not because individual barriers are difficult to escape, but because increasing dimensionality causes an exponential proliferation of local optima that dilutes selection pressure and prevents coordinated multi-dimensional convergence.

---

Across the landscapes studied, a consistent pattern of classical evolutionary behavior emerges. On simple convex landscapes, evolutionary algorithms converge reliably, but this success is uninformative, as no exploration or escape is required. On deceptive landscapes, selection amplifies locally favorable structure, leading to probabilistic but persistent basin capture that mutation and crossover fail to reliably undo. On rugged landscapes such as Rastrigin, increasing dimensionality rapidly dilutes search effort, producing stagnation even when local optima are shallow. These failures arise not from poor parameter choices but from structural properties of evolutionary dynamics: reliance on local fitness comparisons, irreversible selection, and finite population sampling. Understanding these failure modes is essential before proposing alternative mechanisms, as it clarifies what properties any new approach would need to address—and motivates further investigation without assuming that those properties are naturally satisfied by quantum or other non-classical dynamics.
