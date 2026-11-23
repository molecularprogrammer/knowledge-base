---
schema_version: "1.0.0"
id: "mpkb:document:doc-088"
type: reference
title: "Molecular Programming Hardware Tools"
description: "Curated inventory of advanced commercial and open-source hardware used to synthesize, manipulate, automate, and characterize molecular systems."
topics: ["projects", "interfaces", "software-tools"]
keywords: ["laboratory hardware", "DNA synthesis", "liquid handling", "microscopy", "open-source hardware"]
status: published
relationships: []
sources:
  - id: "source:hardware-dnascript-syntax"
    url: "https://www.dnascript.com/resources/"
    title: "SYNTAX Platform product information"
    accessed: 2026-11-23
  - id: "source:hardware-linkzill-trusynth"
    url: "https://www.linkzill.com/en/oligo_microarray_synthesizer/"
    title: "TruSynth oligonucleotide microarray synthesizer"
    accessed: 2026-11-23
  - id: "source:hardware-openids2-repository"
    url: "https://github.com/regiregire/OpenIDS2"
    title: "OpenIDS2 open-source inkjet DNA synthesizer repository"
    accessed: 2026-11-23
  - id: "source:hardware-openids2-paper"
    url: "https://doi.org/10.1371/journal.pone.0338478"
    title: "OpenIDS2: A low-cost, 3D-printed, open-source platform for reproducible construction of DNA microarray synthesizers"
    published: 2025-12-18
    accessed: 2026-11-23
  - id: "source:hardware-hamilton-vantage"
    url: "https://www.hamiltoncompany.com/Microlab-VANTAGE"
    title: "Microlab VANTAGE 2.0 liquid handler"
    accessed: 2026-11-23
  - id: "source:hardware-opentrons-flex"
    url: "https://opentrons.com/products/opentrons-flex-robot"
    title: "Opentrons Flex liquid-handling robot"
    accessed: 2026-11-23
  - id: "source:hardware-opentrons-flex-open-source"
    url: "https://docs.opentrons.com/flex/open-source/"
    title: "Opentrons Flex open-source software documentation"
    accessed: 2026-11-23
  - id: "source:hardware-findus-paper"
    url: "https://doi.org/10.1177/2472630319877374"
    title: "FINDUS: An Open-Source 3D Printable Liquid-Handling Workstation for Laboratory Automation in Life Sciences"
    published: 2020-04-01
    accessed: 2026-11-23
  - id: "source:hardware-jubilee-specs"
    url: "https://jubilee3d.com/index.php?title=Specs"
    title: "Jubilee V2.1 specifications"
    accessed: 2026-11-23
  - id: "source:hardware-science-jubilee"
    url: "https://github.com/Jubilee-CSL/science_jubilee"
    title: "Science Jubilee software for controlling Jubilee platforms"
    accessed: 2026-11-23
  - id: "source:hardware-opendrop"
    url: "https://github.com/GaudiLabs/OpenDrop"
    title: "OpenDrop digital microfluidics project"
    accessed: 2026-11-23
  - id: "source:hardware-openflexure"
    url: "https://openflexure.org/projects/microscope/"
    title: "OpenFlexure Microscope project"
    accessed: 2026-11-23
  - id: "source:hardware-bruker-nanowizard"
    url: "https://www.bruker.com/en/products-and-solutions/microscopes/bioafm/jpk-nanowizard-v-bioscience.html"
    title: "NanoWizard V BioScience atomic force microscope"
    accessed: 2026-11-23
  - id: "source:hardware-automated-afm"
    url: "https://doi.org/10.1016/j.ohx.2023.e00447"
    title: "Automation of an atomic force microscope via Arduino"
    published: 2023-06-29
    accessed: 2026-11-23
  - id: "source:hardware-thermo-glacios"
    url: "https://www.thermofisher.com/us/en/home/electron-microscopy/products/transmission-electron-microscopes/glacios-cryo-tem.html"
    title: "Glacios 3 Cryo-TEM"
    accessed: 2026-11-23
  - id: "source:hardware-thermo-krios"
    url: "https://www.thermofisher.com/us/en/home/electron-microscopy/products/transmission-electron-microscopes/krios-cryo-tem.html"
    title: "Krios 5 Cryo-TEM"
    accessed: 2026-11-23
  - id: "source:hardware-nanomi"
    url: "https://www.cnrc.canada.ca/en/research-development/nanomi-worlds-first-open-source-transmission-electron-microscope"
    title: "NanoMi open-source transmission electron microscope"
    accessed: 2026-11-23
---

# Molecular Programming Hardware Tools {#mpkb:section:sec-1052}

This page lists specific instruments, assemblies, and open hardware projects that can support
molecular programming research. It complements the [software tools catalog](software_tools.md),
which lists software rather than physical devices.

## Selection intent and limits {#mpkb:section:sec-1053}

The intent is to show the most capable and relevant devices currently identified, not to rank every
product on the market. Include advanced commercial devices where they set a useful capability
reference. Also include the leading documented open-source device or design in each relevant class,
even when it has lower throughput, performance, maturity, or support. Do not omit an open option only
because a commercial product is more capable.

“Open-source” applies only to the design elements released under an identified license. Open software
or firmware does not make a proprietary robot an open-hardware design. Research prototypes and
community build projects are not turnkey commercial instruments. Their demonstrated results do not
establish production readiness or independent validation.

Specifications identified as vendor-reported are manufacturer claims, not independent comparisons.
Capabilities can depend on reagents, accessories, protocols, sample preparation, and configuration.
This is a curated snapshot reviewed on 2026-11-23; verify current model availability, software, and
license terms before purchase, construction, or use.

## DNA and oligonucleotide synthesis {#mpkb:section:sec-1054}

| Device or project | Type and use | Reported capability and status |
| --- | --- | --- |
| [SYNTAX System, Model STX-200](https://www.dnascript.com/products/) | Commercial benchtop, template-free enzymatic DNA synthesizer. | DNA Script lists 96-oligo runs as standard; its kits specify different lengths and some 384-well configurations. For example, the 96 Hi-Fidelity kit supports up to 120 nt. Capacity and length depend on the selected kit. These are vendor specifications. |
| [TruSynth oligonucleotide microarray synthesizer](https://www.linkzill.com/en/oligo_microarray_synthesizer/) | Commercial TFT-array electrochemical oligonucleotide microarray synthesizer. | LinkZill describes 4K and 59K/65K feature configurations. It reports a 150-nt evaluation with a 65K-feature oligo pool under a specified amplification and sequencing workflow. Treat throughput and quality figures as vendor-reported and configuration-dependent. |
| [OpenIDS2](https://github.com/regiregire/OpenIDS2) | Open-source, inkjet-based research synthesizer using phosphoramidite chemistry; repository includes 3D-printable mechanical parts, electronics, firmware, and a Python GUI. The repository is marked MIT; verify notices for individual files and dependencies. | The 2025 paper reports synthesis of a 15-mer poly(dT). It estimates mean per-step coupling efficiency at approximately 96.1%; HPLC measured 53.7% full-length product area, with shorter byproducts. This is a research prototype, not a turnkey product. |

## Automated liquid handling and toolchanging {#mpkb:section:sec-1055}

| Device or project | Type and use | Reported capability and status |
| --- | --- | --- |
| [Hamilton Microlab VANTAGE 2.0](https://www.hamiltoncompany.com/Microlab-VANTAGE) | Commercial automated liquid-handling workstation for configurable laboratory workflows. | Hamilton's advanced VANTAGE platform. Select the configuration, channels, labware, and options to match the assay; performance depends on configuration and workflow. |
| [Opentrons Flex](https://opentrons.com/products/opentrons-flex-robot) | Commercial modular liquid-handling robot for sample preparation, PCR, nucleic-acid extraction, and related workflows. | Pipettes, a gripper, modules, and labware are configurable. Opentrons releases Flex software and firmware under open-source licenses, but the robot's hardware design is not thereby open source. Check each repository's license. |
| [FINDUS](https://doi.org/10.1177/2472630319877374) | Published, open-source, 3D-printable liquid-handling workstation. | The paper reports a sub-$400 build and relative pipetting errors below 0.3% for its evaluated setup. This is a laboratory build project, not a supported commercial product; performance depends on assembly, calibration, and protocol. |
| [Jubilee V2.1](https://jubilee3d.com/index.php?title=Specs) with [Science Jubilee](https://github.com/Jubilee-CSL/science_jubilee) | Open-source modular motion and toolchanging platform, with software for controlling lab-oriented Jubilee setups. | The Jubilee project publishes hardware designs under CC BY. Science Jubilee's core control software is MIT-licensed; specific tool hardware, lab decks, and vision plugins are separate projects and are not bundled as a complete liquid-handling system. Requires fabrication, integration, and validation. |

## Digital microfluidics {#mpkb:section:sec-1056}

| Device or project | Type and use | Reported capability and status |
| --- | --- | --- |
| [OpenDrop](https://github.com/GaudiLabs/OpenDrop) | Open-source digital microfluidics research platform. The project provides controller and design files under GPL-3.0 and uses electrowetting to move small liquid droplets. | A community research design for experimentation with lab-on-chip workflows, not a validated turnkey instrument. Confirm the current revision, bill of materials, and performance in the project repository before building. |

## Microscopy and structural characterization {#mpkb:section:sec-1057}

| Device or project | Type and use | Reported capability and status |
| --- | --- | --- |
| [NanoWizard V BioScience](https://www.bruker.com/en/products-and-solutions/microscopes/bioafm/jpk-nanowizard-v-bioscience.html) | Commercial automated quantitative BioAFM for nanomechanical imaging of single molecules, cells, tissues, and delicate samples, with optical-microscope integration. | Bruker advertises automated setup and scanning up to 400 lines/s. These are vendor-reported capabilities; actual results depend on sample and configuration. |
| [Glacios 3 Cryo-TEM](https://www.thermofisher.com/us/en/home/electron-microscopy/products/transmission-electron-microscopes/glacios-cryo-tem.html) | Commercial 200 kV cryo-TEM for single-particle analysis, cryo-electron tomography, and microcrystal electron diffraction. | High-end, facility-scale instrument with substantial infrastructure, sample-preparation, and operating requirements. |
| [Krios 5 Cryo-TEM](https://www.thermofisher.com/us/en/home/electron-microscopy/products/transmission-electron-microscopes/krios-cryo-tem.html) | Commercial high-end cryo-TEM for single-particle analysis, cryo-electron tomography, and microcrystal electron diffraction. | Facility-scale instrument intended for high-throughput structural biology. Manufacturer performance claims depend on workflow and configuration. |
| [NanoMi](https://github.com/NanoMi-org/NanoMi) | Open-source modular electron-microscope platform. The published design supports TEM, STEM, SEM, and electron-diffraction configurations. | The NRC describes a 50 keV design with a target resolution near 10 nm. It is a build-and-customize research platform, not a turnkey commercial microscope; the first prototype used a separately sourced commercial electron gun. It is not a cryo-TEM. |
| [Automated AFM (Dimension 3000 retrofit)](https://doi.org/10.1016/j.ohx.2023.e00447) | Published open-hardware Arduino retrofit that motorizes sample positioning and automates image acquisition on a Bruker Dimension 3000 AFM. The released designs are CC BY-SA 4.0. | The paper reports an under-$60 add-on and sub-micron positioning for the tested setup. It requires an existing compatible AFM, adaption to that instrument, and has positioning backlash; it is not a standalone AFM. |
| [OpenFlexure Microscope](https://openflexure.org/projects/microscope/) | Open-source, customizable optical microscope and motorized positioning stage. Most structural parts can be 3D-printed; optics can range from webcam-based to standard microscope objectives. | A strong open-source option for optical imaging and positioning, including optional fluorescence configurations. It is not an AFM or electron microscope and cannot replace nanoscale surface or cryogenic structural imaging. Project design is CC BY-SA 4.0; purchased optics and electronics retain their own terms. |

No directly comparable open-source design for high-end cryo-TEM was identified for this curated list.
NanoMi and the AFM retrofit are open designs for different use cases; do not treat them as performance
equivalents to commercial high-end cryo-TEM or BioAFM systems.

## Cross-cutting use {#mpkb:section:sec-1058}

Hardware choices connect to the application and experiment, not only to an instrument category:

- The [software tools catalog](software_tools.md) lists design and analysis software that may pair
  with these devices.
- The [developer tools roadmap](developer_tools_roadmap.md) describes how to join design, production,
  measurement, and verification into repeatable workflows.
- [Interfaces and experimental methods](../research_topics/interfaces/index.md) covers synthesis,
  measurement, and device integration methods.
- [Structures and dynamics](../research_topics/structures_and_dynamics/index.md) covers systems and
  assemblies that these instruments can fabricate or characterize.

Before use, define the intended sample, measurable output, controls, calibration, operating conditions,
and acceptance criteria. Record exact model, accessories, software/firmware version, protocol, and
limitations with each experimental result.