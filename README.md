
# Quantum Interference vs Evolutionary Search

*(A mechanism-first investigation)*

**Core question**: Does raw quantum coherence (superposition + interference) naturally aid evolutionary escape from deceptive/rugged fitness landscapes....or does it conflict?

## Key Findings
- Classical GA baselines: basin capture (deceptive), info dilution (rugged)
- Superposition alone ≡ classical uniform sampling (no gain)
- Naive fitness→phase interference *worsens* deception
- Unitary dynamics amplify structure; evolution needs irreversible breaking

**Conclusion**: Quantum success requires classical scaffolding. [Full report → `./docs/overview.md`]

## Repo Structure
├── docs/ # Full analysis + derivations

├── code/ # Classical + quantum experiments

│ ├── classical/ # GA baselines

│ └── quantum/ # Superposition + interference

├── figures/ # some visuals

├── notes/ # personal insights



## 4. What is NOT claimed

This project intentionally avoids the usual quantum-optimization claims. In particular, it does **not** assume or invoke:

* a full quantum genetic algorithm
* algorithmic speedup or complexity advantages
* tunneling-based barrier traversal
* superiority over classical heuristics
* relevance to near-term quantum hardware

The absence of these claims is deliberate: **the goal is not to argue that a quantum algorithm works, but to test whether the physics itself supports the intuition that it should.**

## A note on conclusions and method

It is possible today to obtain a plausible, high-level answer to the small question “Does quantum coherence aid evolutionary search?” by simply prompting LLMs. Such answers often gesture toward decoherence, noise, and irreversibility.

This project begins where those answers end.

Rather than relying on intuition or analogy, the work here isolates quantum mechanisms under controlled conditions and examines their concrete effects on known evolutionary failure modes. Several of the results—most notably cases where interference actively worsens deception—do not follow from the headline conclusion alone and only become visible through explicit construction and experiment.

The goal is therefore not novelty of outcome, but clarity of boundary: identifying which parts of successful quantum-inspired optimization are genuinely quantum, and which depend on classical mechanisms that explicitly break coherence.

---

