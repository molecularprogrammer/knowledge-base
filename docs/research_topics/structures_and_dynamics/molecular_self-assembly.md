---
schema_version: "1.0.0"
id: "mpkb:document:doc-084"
type: article
title: "Molecular Self-Assembly"
description: "Explains how designed molecular components organize into larger structures through local interactions, and how design, conditions, and assembly pathways affect the outcome."
topics: ["structures-and-dynamics", "dna-nanotechnology"]
keywords: ["supramolecular chemistry", "DNA nanotechnology", "molecular recognition"]
status: published
relationships:
  - type: related
    target: "mpkb:document:doc-049"
  - type: related
    target: "mpkb:document:doc-045"
  - type: related
    target: "mpkb:document:doc-052"
  - type: related
    target: "mpkb:document:doc-085"
  - type: related
    target: "mpkb:document:doc-068"
sources:
  - id: "source:molecular-self-assembly-2021"
    url: "https://doi.org/10.1021/acs.chemrev.1c00884"
    title: "Introduction: Molecular Self-Assembly"
    authors: ["D. Pochan", "O. Scherman"]
    published: 2021-11-24
  - id: "source:dna-origami-primer-2011"
    url: "https://doi.org/10.1038/nmeth.1570"
    title: "A primer to scaffolded DNA origami"
    authors: ["C. E. Castro", "F. Kilchherr", "D.-N. Kim", "E. L. Shiao", "T. Wauer", "P. Wortmann", "M. Bathe", "H. Dietz"]
    published: 2011-02-25
---

# Molecular Self-Assembly {#mpkb:section:sec-0222}

Molecular self-assembly is the organization of molecular building blocks into larger, ordered
structures through their interactions and the conditions of their environment. The design task is
not only to choose components that bind. It is also to make the intended structure more favorable
than competing structures and to provide conditions under which the system can reach it.

## Building Blocks and Interactions {#mpkb:section:sec-0224}

Building blocks may be small molecules, polymers, nucleic acids, proteins, or pre-assembled
nanostructures. Their recognition and association can use hydrogen bonding, electrostatic forces,
base pairing, hydrophobic effects, metal coordination, shape complementarity, or combinations of
these interactions. Interaction strength, directionality, and reversibility affect which structures
form and whether errors can be corrected.

DNA nanostructures provide one example of programmable recognition: complementary sequences can
specify local connections, while strand routing and scaffold design constrain the overall shape.
Other systems use designed host–guest pairs, peptides, amphiphiles, or coordination motifs.

## Assembly Pathways and Conditions {#mpkb:section:sec-0225}

Assembly depends on both the final structure's stability and the pathway by which components meet
and rearrange. Concentration, temperature, solvent, ionic strength, pH, surfaces, and mixing can
change rates, intermediate populations, and product distributions. Some systems approach an
equilibrium distribution. Others become kinetically trapped in structures that persist even when a
different arrangement would be more stable.

Reversible interactions can allow misbound components to dissociate and rearrange. Excessively weak
interactions may not hold the product together; excessively strong or poorly positioned interactions
can trap incorrect intermediates. Experiments should therefore assess yield, structural fidelity,
kinetics, and robustness to changes in conditions.

## Design and Characterization {#mpkb:section:sec-0226}

Design typically proceeds by specifying a target structure or function, choosing compatible
building blocks and interaction rules, and testing candidate conditions. Computational models can
help predict geometry, energetics, and competing pathways, but model assumptions must be checked
against measurements.

Characterization methods depend on the system and scale. They can include microscopy, spectroscopy,
scattering, electrophoresis, calorimetry, and single-molecule measurements. No single measurement
necessarily establishes both composition and structure, so complementary methods are often needed.

## Scope and Limitations {#mpkb:section:sec-0227}

Self-assembly can create structures that are difficult to build by addressing each component
individually. It does not guarantee a unique product, high yield, or function. Defects, aggregation,
off-target binding, slow assembly, sensitivity to environmental conditions, and scale-up can limit
performance. A useful design should identify these failure modes and define measurements that can
distinguish successful assembly from nonspecific association.

## Related Topics {#mpkb:section:sec-0228}

- [Supramolecular chemistry](supramolecular.md)
- [Nucleic acid hybridization](nucleic_acid_hybridization.md)
- [Molecular walkers](molecular_walkers.md)
- [Templated assembly](../theoretical_foundations/templated_assembly.md)

## Sources {#mpkb:section:sec-0229}

- Pochan, D. and Scherman, O. (2021). [Introduction: Molecular Self-Assembly](https://doi.org/10.1021/acs.chemrev.1c00884). *Chemical Reviews*, 121(22), 13699–13700.
- Castro, C. E., Kilchherr, F., Kim, D.-N., Shiao, E. L., Wauer, T., Wortmann, P., Bathe, M. and Dietz, H. (2011). [A primer to scaffolded DNA origami](https://doi.org/10.1038/nmeth.1570). *Nature Methods*, 8, 221–229.