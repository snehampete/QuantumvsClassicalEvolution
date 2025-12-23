
## Conceptual clarifications gained from the parabolic case

Although the parabolic landscape is trivial from an optimization standpoint, working through it surfaced several important conceptual clarifications that shaped how the classical algorithm should be interpreted on harder landscapes.

### 1. Elitism preserves information; it does not generate exploration

A key realization was that elitism does **not** help the population explore the landscape. It merely guarantees that the best solutions already discovered are not lost due to stochastic effects in selection or mutation.

On the parabolic landscape, this distinction is invisible because the global optimum lies in the same basin as every initial point. However, this insight becomes critical later: elitism stabilizes convergence but can also lock the population into whichever basin it has already entered.

---

### 2. Selection and crossover alone cannot create novelty

Another important clarification was understanding that tournament selection and crossover only **rearrange existing population structure**. They do not introduce fundamentally new information.

On a convex landscape, recombining partially good solutions naturally yields better ones, so this limitation is hidden. But the parabolic case made it clear that without mutation (or some equivalent mechanism), the algorithm cannot escape the span of what it has already sampled.

---

### 3. Mutation is the sole source of true exploration in classical GA

By explicitly disabling mutation, it became clear that the population rapidly collapses to a single value and then remains fixed. This highlighted that, in classical evolutionary algorithms, mutation is the **only mechanism capable of generating new candidate regions** of the search space.

On the parabola, even very weak mutation suffices because any small perturbation toward the center improves fitness. This foreshadows why mutation becomes ineffective on landscapes with deep valleys or narrow barriers.

---

### 4. Apparent “theoretical behavior” can arise from implementation edge cases

While experimenting with edge parameter values (e.g., zero elitism), an initially puzzling “memoryless” behavior was observed. This ultimately traced back to a slicing edge case in the implementation rather than a property of evolutionary dynamics.

This reinforced an important methodological lesson: **algorithmic conclusions must be separated from implementation artifacts**, especially when studying failure modes. This insight motivated a systematic audit of boundary conditions before proceeding to harder landscapes.

---

### 5. Success on convex landscapes is structurally guaranteed

The parabolic case clarified that success here is not evidence of algorithmic power. Rather, it is a consequence of the alignment between:

* fitness gradients,
* selection pressure, and
* local variation mechanisms.

Because every direction “uphill” points toward the same optimum, convergence is inevitable and uninformative. This realization sharpened the motivation for studying deceptive and multimodal landscapes, where such alignment breaks down.

---


