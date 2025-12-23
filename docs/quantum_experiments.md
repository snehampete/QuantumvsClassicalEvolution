
# Quantum Experiments

**Isolating superposition and interference**

---

## 1. Why minimal quantum mechanisms

The goal of the quantum experiments in this project is **not** to construct a full quantum evolutionary algorithm, nor to benchmark performance against classical methods. Instead, the objective is to **isolate and test individual quantum mechanisms**—specifically superposition and interference—to determine whether they naturally align with the requirements of evolutionary search.

Full quantum genetic algorithms typically combine multiple effects at once: selection, mutation, measurement, noise, and heuristic tuning. When such systems succeed or fail, it is often unclear which component is responsible. This project deliberately avoids that ambiguity.

By testing minimal mechanisms in controlled settings, we ask a more fundamental question:
**what does quantum mechanics itself contribute, before any algorithmic scaffolding is added?**

---

## 2. Experiment 1: Superposition + measurement

### Setup

A uniform quantum superposition is constructed over a discretized search space. Each position is assigned equal amplitude, and no fitness or structural information is encoded. Measurement outcomes are sampled according to the Born rule.

This setup mirrors classical uniform random sampling, but implemented through quantum state preparation and measurement.

---

### Result

Measurement statistics from the quantum superposition are indistinguishable from classical uniform sampling. Basin occupancy and sampling frequencies match classical expectations within statistical noise.

---

### Interpretation

Superposition alone does not provide enhanced exploration. In the absence of interference or structure-dependent encoding, quantum measurement reproduces classical randomness. This result establishes a necessary baseline: **quantum superposition by itself does not alter evolutionary behavior**.

---

## 3. Experiment 2: Phase without interference (control)

### Setup

Relative phases are assigned to basis states while keeping amplitude magnitudes fixed and equal. No unitary mixing or basis change is applied prior to measurement.

This experiment tests whether phase information alone can influence measurement outcomes.

---

### Result

Measurement statistics remain unchanged from the uniform superposition case. Phase encoding without subsequent mixing produces no observable effect.

---

### Interpretation

Global or relative phase is not directly observable. Without a unitary transformation that forces amplitudes to interfere, phase information has no measurable consequence. This control confirms that **interference—not phase itself—is the relevant non-classical mechanism**.

---

## 4. Experiment 3: Naive phase-based interference

### Setup

Fitness values are mapped directly to phases, and a global unitary mixing operator (discrete Fourier transform) is applied to induce interference. Measurement outcomes are then sampled via the Born rule.

This setup implements the most common intuitive mapping: **higher fitness → larger phase contribution**.

---

### Observed failure

Rather than suppressing deceptive basins, interference systematically biases sampling **toward the wrong basin**. The effect is stable, monotonic with phase strength, and reproducible across trials.

This represents a clear failure mode, not random noise.

---

### Explanation

The failure arises from multiple interacting factors:

* **Phase periodicity**: phase wraps modulo (2\pi), while fitness magnitude is unbounded. Large fitness gradients induce rapid phase oscillation and dephasing.
* **Smoothness bias**: interference favors phase-coherent regions rather than tall or narrow peaks.
* **Misalignment with fitness magnitude**: fitness height does not correspond to phase stability, causing deceptive basins to dominate.

This experiment demonstrates that **naive fitness-to-phase encodings can actively worsen evolutionary trapping**.

---

## 5. Rank-based phase control

### Why this encoding was tested

To determine whether the failure above was caused by magnitude information rather than ordering, fitness ranks were encoded into phase. This preserves relative ordering while eliminating scale and wrapping pathologies.

The rank-based encoding serves as a diagnostic control, not an attempted improvement.

---

### Result

Rank-based phase encoding removes the destructive bias observed in magnitude-based encoding. Sampling becomes approximately symmetric between basins, matching classical behavior.

No consistent bias toward the global optimum is observed.

---

### Interpretation

Encoding ordering information avoids phase incoherence but does not introduce constructive guidance. This indicates that **ordinal fitness structure alone is insufficient for interference-driven search**. Interference becomes neutral rather than harmful, but still does not generate escape.

---

## 6. Summary of quantum findings

Across all quantum experiments:

* Superposition reproduces classical sampling.
* Phase without interference has no observable effect.
* Naive phase-based interference can worsen deceptive trapping.
* Rank-based phase encoding neutralizes harm but provides no advantage.

No quantum speedup, escape mechanism, or optimization benefit is claimed. These results demonstrate that **raw quantum coherence does not naturally implement evolutionary exploration**, and that interference aligns with phase structure rather than fitness objectives.

---

### Scope reminder

These experiments intentionally exclude:

* full quantum genetic algorithms
* Grover-style amplification
* hybrid evolutionary loops
* hardware or performance claims

Interpretation and broader implications are discussed separately in `docs/synthesis_and_limits.md`.

---
