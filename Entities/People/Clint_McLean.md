# Clint McLean
**Date Added:** 2025-12-09
**Classification:** RESEARCH ALLY / DETECTION TECHNOLOGY DEVELOPER
**Status:** ACTIVE RESEARCHER
**Priority:** HIGH - Potential Technical Resource

## Overview

**GitHub:** [ClintMclean74](https://github.com/ClintMclean74)
**Twitter:** [@clintmclean74](https://twitter.com/clintmclean74)
**Affiliation:** Mclean Research Institute
**Focus:** RF biological effects detection, Havana Syndrome research, neural modeling

Clint McLean is an independent researcher who has developed open-source tools specifically designed to detect reradiated frequencies that could cause biological effects. His work directly addresses the detection of technology similar to what is documented in this investigation.

---

## Key Projects

### 1. SDR Reradiation Spectrum Analyzer

**Repository:** [SDRReradiationSpectrumAnalyzer](https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer)
**Language:** C (64%), C++ (30.5%)
**Stars:** 5 | Forks: 2

**Purpose:**
Software Defined Radio (SDR) spectrum analyzer designed to detect and analyze reradiated frequency ranges that could be used to cause biological effects.

**Capabilities:**
- Real-time spectrum visualization (2D/3D graphics)
- Automated detection of reradiated frequency ranges
- Multiple scanning modes (normal and sessions-based)
- Signal strength and correlation analysis
- Historical data tracking with results graphs
- Interactive frequency range selection and zoom

**Technical Requirements:**
- RTL-SDR compatible device (USB dongle, ~$25)
- librtlsdr for device communication
- libusb for USB interface
- OpenGL for visualization
- GNU Radio for signal processing

**Research Reference:**
Developer references a thesis documenting "how I detected reradiated frequency ranges that could be used to cause biological effects."

**Relevance to Investigation:**
This tool could potentially be used to detect:
- V2K (Voice-to-Skull) transmissions
- Directed Energy Weapon (DEW) emissions
- RF-based neural stimulation signals
- IoB body area network communications

---

### 2. SDR Spectrum Analyzer

**Repository:** [SDRSpectrumAnalyzer](https://github.com/ClintMclean74/SDRSpectrumAnalyzer)
**Language:** C#
**Stars:** 12 | Forks: 3

Base spectrum analyzer tool for RTL-SDR devices. Foundation for the more specialized reradiation analyzer.

---

### 3. Hodgkin-Huxley Neural Model Code

**Repository:** [Hodgkin-HuxleyCode](https://github.com/ClintMclean74/Hodgkin-HuxleyCode)
**Language:** C (83.6%)
**Copyright:** Clint Mclean, Mclean Research Institute (2022)
**License:** GNU GPL v2+

**Purpose:**
Source code accompanying the book:
> **"Solving Havana Syndrome and Biological Effects of RF Using the Hodgkin-Huxley Neuron Model"**

**What It Does:**
- Simulates neural behavior using Hodgkin-Huxley equations
- Models how action potentials in neurons are initiated and propagated
- Demonstrates RF effects on neural activity
- Provides computational framework for understanding Havana Syndrome mechanism

**The Hodgkin-Huxley Model:**
The foundational mathematical model (Nobel Prize 1963) describing electrical characteristics of neurons. McLean applies this to understanding how RF radiation affects neural function.

**Relevance to Investigation:**
- Directly models the biological mechanism of V2K/DEW attacks
- Provides scientific framework for understanding [[Technical/Internet_of_Bodies_Architecture|IoB]] neural effects
- Could validate or explain symptoms reported by targeted individuals
- Connects to [[Patents/PATENT_MASTER_INDEX|patents]] like US 6,470,214 (V2K) and US 7,740,596 (MEDUSA)

---

## Significance to Investigation

### Detection Capability

McLean's SDR tools could potentially detect:

| Attack Type | Detection Method | Tool |
|-------------|------------------|------|
| V2K signals | RF spectrum analysis | SDRReradiationSpectrumAnalyzer |
| DEW emissions | Reradiation pattern detection | SDRReradiationSpectrumAnalyzer |
| Neural stimulation | Frequency correlation | SDRSpectrumAnalyzer |
| Body area network | Wireless protocol detection | SDRSpectrumAnalyzer |

### Scientific Validation

The Hodgkin-Huxley book provides:
1. **Scientific framework** for understanding how RF causes biological effects
2. **Computational model** that can simulate neural responses to specific frequencies
3. **Havana Syndrome connection** - same technology affecting diplomats and targeted individuals
4. **Peer-reviewable methodology** for legal proceedings

---

## Havana Syndrome Connection

**What is Havana Syndrome?**
- Neurological symptoms reported by U.S. diplomats (Cuba 2016, China, Russia, etc.)
- Symptoms: headaches, dizziness, cognitive difficulties, hearing sounds
- Attributed to directed energy attacks (microwave weapons)
- U.S. government officially acknowledged as attacks

**McLean's Research:**
- Models the neural mechanism of these attacks
- Provides detection methodology
- Offers scientific explanation for symptoms
- Potentially validates targeted individual reports

**Connection to Investigation:**
- [[Patents/PATENT_MASTER_INDEX|Patent US 6,470,214]] (V2K) - Same technology
- [[Patents/PATENT_MASTER_INDEX|Patent US 7,740,596]] (MEDUSA) - Microwave auditory effect
- [[Entities/Dr_James_Giordano|Dr. Giordano]] confirms "weaponized neuroscience" exists
- [[Technical/Internet_of_Bodies_Architecture|IoB Architecture]] includes neural stimulation capability

---

## Potential Collaboration Value

### Technical Resources
- Open-source detection tools (immediate use)
- RTL-SDR hardware requirements (~$25 USB dongle)
- Documentation and installation guides
- Configuration files for various experimental conditions

### Expert Testimony
McLean's research could support [[LEGAL_CASE_FRAMEWORK|legal case]]:
- Expert on RF biological effects
- Published methodology (book + thesis)
- Detection evidence capabilities
- Havana Syndrome scientific framework

### Evidence Gathering
SDR tools could provide:
- Real-time detection of attacks
- Recorded spectrum data (timestamped evidence)
- Frequency correlation to known weapon patents
- Independent verification of targeting

---

## Technical Setup (From Repositories)

### SDRReradiationSpectrumAnalyzer Installation (Linux/Ubuntu)

```bash
# Install dependencies
sudo apt-get install build-essential
sudo apt-get install libgl-dev libglu1-mesa-dev
sudo apt-get install gnuradio gr-osmosdr
sudo apt-get install libusb-1.0-0-dev

# Install RTL-SDR drivers
# Clone repository
git clone https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer.git

# Pre-compiled binaries available in SDRReradiation/bin folder
```

### Hardware Required
- RTL-SDR USB dongle (RTL2832U chipset)
- Cost: ~$25-35
- Available: Amazon, electronics suppliers

---

## Research Questions

1. Has McLean detected specific frequency ranges matching known patents?
2. Does his Hodgkin-Huxley model predict effects matching reported symptoms?
3. Has he collaborated with other targeted individual researchers?
4. What frequencies does his reradiation analyzer flag as concerning?
5. Can his tools detect [[Entities/Apple|Apple Watch]] or [[Entities/FreerLogic|FreerLogic]] emissions?

---

## Action Items

### Immediate
- [ ] Review full thesis referenced in SDRReradiationSpectrumAnalyzer
- [ ] Clone and test SDR tools locally
- [ ] Obtain RTL-SDR hardware for detection testing
- [ ] Contact McLean for potential collaboration

### Short-Term
- [ ] Compare detected frequencies to patent specifications
- [ ] Test detection capability against known IoB devices
- [ ] Review Hodgkin-Huxley book for legal case evidence value
- [ ] Assess expert witness potential

### Legal Relevance
- [ ] Document McLean's methodology for evidence gathering
- [ ] Prepare expert witness inquiry
- [ ] Correlate his findings with [[Evidence Repository|existing evidence]]

---

## External Links

- **GitHub Profile:** https://github.com/ClintMclean74
- **SDRReradiationSpectrumAnalyzer:** https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer
- **SDRSpectrumAnalyzer:** https://github.com/ClintMclean74/SDRSpectrumAnalyzer
- **Hodgkin-HuxleyCode:** https://github.com/ClintMclean74/Hodgkin-HuxleyCode
- **Twitter:** https://twitter.com/clintmclean74
- **3D Models (Sketchfab):** https://sketchfab.com/clintmclean74/collections

---

## Conclusion

Clint McLean represents a potentially valuable technical ally for the investigation:

1. **Detection Tools:** Open-source SDR analyzers could gather evidence of RF attacks
2. **Scientific Framework:** Hodgkin-Huxley modeling provides legal/scientific validation
3. **Havana Syndrome Link:** Bridges targeted individual reports to officially acknowledged attacks
4. **Expert Resource:** Published researcher with documented methodology

**Recommendation:** Establish contact, test detection tools, assess collaboration potential.

---

**Priority:** HIGH - Technical Resource
**Status:** Profile Documented
**Category:** Research Ally
**Last Updated:** 2025-12-09

## Related Files

- [[Technical/Internet_of_Bodies_Architecture]] - IoB detection targets
- [[Patents/PATENT_MASTER_INDEX]] - Patent frequencies to detect
- [[Entities/Dr_James_Giordano]] - Confirms weapons exist
- [[LEGAL_CASE_FRAMEWORK]] - Expert witness potential
- [[Evidence Repository]] - Detection data storage
- [[Analysis/Threat Assessment]] - Detection as countermeasure
