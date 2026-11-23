---
schema_version: "1.0.0"
id: "mpkb:document:doc-089"
type: article
title: "Energy and Feedstock Inputs for Biological Systems"
description: "Distinguishes energy supplies from material feedstocks and surveys biological and hybrid systems that convert them into products."
topics: ["systems", "energy"]
keywords: ["energy supply", "energy harvesting", "feedstock", "acetate", "electro-agriculture"]
status: published
relationships:
  - type: related
    target: "mpkb:document:doc-077"
  - type: related
    target: "mpkb:document:doc-056"
sources:
  - id: "source:electro-agriculture-acetate-2022"
    url: "https://doi.org/10.1038/s43016-022-00530-x"
    title: "A hybrid inorganic–biological artificial photosynthesis system for energy-efficient food production"
    authors: ["Elizabeth C. Hann", "Sean Overa", "Marcus Harland-Dunaway", "Andrés F. Narvaez", "Dang N. Le", "Martha L. Orozco-Cárdenas", "Feng Jiao", "Robert E. Jinkerson"]
    published: 2022-06-23
---

# Energy and Feedstock Inputs for Biological Systems {#mpkb:section:sec-1059}

Biological and hybrid systems need both **energy** to drive processes and **matter** to build
products. These inputs can come from the environment or from supplied resources. Keeping the two
roles distinct helps describe what a device or organism actually consumes, converts, and produces.

## Energy and Material Inputs {#mpkb:section:sec-1060}

Energy may be captured from light, mechanical motion or vibration, temperature differences, or
electromagnetic radiation. Chemical reactions can also supply usable energy. The conversion device
may store energy before use, for example in a battery or chemical carrier. Alternatively, a system
may receive electricity directly from a battery, power supply, or electrical outlet. Supplied power
does not require the device itself to harvest ambient energy.

Feedstocks are material inputs used to make biomass or products. They can include carbon sources,
nutrients, water, and electron donors. A substance can have more than one role: acetate can supply
carbon atoms and support cellular metabolism in organisms that can use it. However, supplying a
feedstock is not the same as supplying electricity, and a complete process may require both material
and energy inputs.

## Electro-Agriculture and Acetate {#mpkb:section:sec-1061}

Electro-agriculture explores routes that use electrical energy to convert carbon dioxide and water
into compounds that biological systems can use as feedstocks. One demonstrated laboratory pathway
uses a two-step CO₂ electrolyser to produce an acetate-rich stream. The electrical input powers the
electrolysis; acetate is the resulting carbon-containing product and biological substrate.

Hann et al. (2022) reported a system with 57% carbon selectivity from CO₂ to acetate. They used the
acetate stream for heterotrophic cultivation of yeast, a mushroom-producing fungus, and a green alga
in the dark. They also found that carbon from externally supplied acetate entered biomass through
major metabolic pathways in tests involving nine crop plants. These are distinct results: growth of
the three tested organisms on acetate was demonstrated, while the crop-plant evaluation showed
acetate-carbon incorporation and does not by itself demonstrate complete crop production without
photosynthesis.

The authors proposed coupling the process to photovoltaic electricity as a way to improve
solar-to-food conversion. This is a system-level opportunity, not evidence that the electrolyser
harvests ambient energy on its own or that a complete field-scale food-production system has been
established. In any implementation, electricity source, conversion efficiency, acetate yield and
purity, organism compatibility, nutrient supply, and downstream processing all affect performance.

## Design Questions {#mpkb:section:sec-1062}

When describing an energy-dependent biological system, identify each input and conversion:

- What provides process energy: ambient energy capture, stored energy, chemical energy, or supplied
  electricity?
- What material feedstocks supply carbon, nutrients, and other atoms in the product?
- Which component converts one input into another, and what are its measured outputs and losses?
- Does the organism use a substrate for carbon, metabolic energy, or both?
- Which steps have been demonstrated, and which are proposed integrations or scale-up goals?

These questions apply to electro-agriculture and to other molecular-programming systems that combine
energy conversion, biological production, and external control.

## Related Topics {#mpkb:section:sec-1063}

- [Energy applications](../../what_is_molecular_programming/example_applications/energy.md)
- [Engineering biological circuits](engineering_biological_circuits.md)
- [Generative optogenetics](generative_optogenetics.md)
- [Interfaces and experimental methods](../interfaces/index.md)

## Further Reading {#mpkb:section:sec-1064}

- Hann et al. (2022). “A hybrid inorganic–biological artificial photosynthesis system for
  energy-efficient food production.” *Nature Food*, 3, 461–471.
  [https://doi.org/10.1038/s43016-022-00530-x](https://doi.org/10.1038/s43016-022-00530-x).
