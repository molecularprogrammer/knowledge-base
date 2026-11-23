---
schema_version: "1.0.0"
id: "mpkb:document:doc-086"
type: index
title: "Theoretical Foundations"
description: "Overview of models, algorithms, physical principles, and analysis methods used to reason about molecular systems."
topics: ["theoretical-foundations"]
keywords: []
status: published
relationships: []
sources: []
---

# Theoretical Foundations {#mpkb:section:sec-1032}

This area covers concepts and methods used to describe molecular systems, predict their behavior,
and reason about what they can compute. These foundations connect to experimental work, molecular
circuits, and system-level design.

## Models and Algorithms {#mpkb:section:sec-1033}

Computational models and algorithms describe how molecular systems can represent information,
perform operations, and reach outcomes under physical constraints.

- [Algorithm design for molecular systems](algorithm_design.md)
- [Algorithms at the molecular scale](algorithms_at_molecular_scale.md)
- [Computational models for molecular systems](formal_language_theory/computational_models.md)
- [Computational limits](complexity_theory/computational_limits.md)
- [Information encoding](information_theory/molecular_encoding.md)

The two algorithm pages have closely related scope. The first concerns how to design algorithms
for molecular systems; the second concerns how those algorithms are implemented by molecular-scale
processes. Keep this distinction clear as the pages are developed.

## Dynamics, Uncertainty, and Physical Models {#mpkb:section:sec-1034}

Reaction networks, diffusion, and stochastic behavior connect idealized designs to physical
operation. These topics also inform circuit and system design.

- [Stochastic modeling of chemical reaction networks](chemical_reaction_networks/stochastic_modeling.md)
- [Reaction-diffusion systems](chemical_reaction_networks/reaction_diffusion_systems.md)
- [Molecular noise](molecular_noise.md)
- [Quantum effects in molecular systems](quantum_effects.md)

For applications of these models to information processing, see [Molecular Circuits](../circuits/index.md).