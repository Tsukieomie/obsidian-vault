# Clint McLean
**Date Added:** 2025-12-09
**Classification:** RESEARCH ALLY / DETECTION TECHNOLOGY DEVELOPER
**Status:** ACTIVE RESEARCHER
**Priority:** HIGH - Potential Technical Resource

## Overview

**GitHub:** [ClintMclean74](https://github.com/ClintMclean74)
**Twitter:** [@clintmclean74](https://twitter.com/clintmclean74)
**Website:** [McLean Research Institute](https://mcleanresearchinstitute.com)
**Affiliation:** Mclean Research Institute
**Focus:** RF biological effects detection, Havana Syndrome research, neural modeling

Clint McLean is an independent researcher who has developed open-source tools specifically designed to detect reradiated frequencies that could cause biological effects. His work directly addresses the detection of technology similar to what is documented in this investigation.

---

## Published Work

### Book: "Solving Havana Syndrome and Biological Effects of RF Using the Hodgkin-Huxley Neuron Model"

**Available:** [Amazon Kindle](https://www.amazon.com/Solving-Syndrome-Biological-Effects-Hodgkin-Huxley-ebook/dp/B0BCNG8H89)
**Also:** [Google Books](https://books.google.com/books/about/Solving_Havana_Syndrome_and_Biological_E.html?id=6IP_zwEACAAJ)
**Publisher:** Mclean Research Institute (2022)

**Key Claims:**
> "This work solves the scientific question of how radio and microwave energy could cause the various neurological symptoms of Havana Syndrome experienced by officials in Cuba, China and elsewhere, without the experience of a burning sensation on the skin's surface."

**Paradigm Shift:**
> "The results of this work creates a paradigm shift in our understanding of the biological effects of sub-thermal RF energy. Scientists have been searching for the mechanism that results in sub-thermal effects on biology for many years. This work solves this mystery."

**Core Mechanism Described:**
The book describes a mechanism that "directly converts electromagnetic energy into neuron membrane voltage changes, thus affecting neurological signalling and causing the various symptoms of Havana Syndrome."

### Key Scientific Concepts from Book

**1. Anode Break Excitation**
- A reviewer found this concept "eye-opening to activation effects"
- Anode break excitation (ABE) is when a neuron fires action potentials in response to the termination of a hyperpolarizing current
- When anodal stimulus ends, membrane potential overshoots resting level, causing sodium channels to open and generate a spike
- The Hodgkin-Huxley model accurately predicts this phenomenon
- **Significance:** Explains how pulsed RF can trigger neural activity

**2. Summation Effect**
McLean states: "The effects of the RF energy is effectively summed at each neuron and all its connected neurons."
- Reviewer notes this is "an important insight as to how coherence and synchronization across the whole of the brain and how RF weapons affect victims neurologically"

**3. Rate Coding Disruption**
McLean quotes Kilian Koepsell et al (Frontiers in Neuroscience) on rate coding:
- "Spike rates affect information being transmitted"
- "It is possible it is disruptive to synchronization"

### Research Paper (2019)

**Title:** "Detection of Frequencies that could be used for Electronic Harassment and Electrosensitivity"
**Code:** https://github.com/ClintMclean74/SDRSpectrumAnalyzer
**User Guide:** [Google Drive](https://drive.google.com/file/d/1GixkhAa6bBUuEGLTBrWXw7OFkZQBzuxV/view)

---

## Complete GitHub Repository Analysis

### Overview of All Repositories

| Repository | Language | Stars | Forks | Last Updated |
|------------|----------|-------|-------|--------------|
| SDRSpectrumAnalyzer | C# (86.2%) | 12 | 3 | May 2019 |
| SDRReradiationSpectrumAnalyzer | C (64%) | 5 | 2 | Oct 2023 |
| Hodgkin-HuxleyCode | C (83.6%) | - | - | Oct 2024 |
| ClintMclean74 | Config | - | - | Feb 2022 |

---

## Repository 1: SDRSpectrumAnalyzer (Original - Windows)

**Repository:** [SDRSpectrumAnalyzer](https://github.com/ClintMclean74/SDRSpectrumAnalyzer)
**Language:** C# (86.2%), C++ (4.3%), C (2.7%)
**License:** GNU GPL v2.0
**Commits:** 54

### Purpose
> "RTL SDR Spectrum Analyzer for Detection of Reradiated and Emitted Radio and Microwave Energy from Humans"

### Core Detection Principle

The system identifies reradiated signals by monitoring whether RF signal strength **increases when a user is near their computer and antenna**. It uses keyboard/mouse activity to determine proximity.

**Key Insight:**
> "Finding your reradiated frequency range could be very important for determining how that frequency range is being used and whether there are transmissions that could be causing unintentional (electrosensitivity) or intentional biological effects."

### Signal Analysis Process

1. **Averaging:** Signal strength averaged over longer periods to reduce noise
2. **Leaderboards:** Ranks signals by frequency of detection
3. **1 MHz Prioritization:** Prioritizes frequency bands containing candidate signals
4. **Transition Analysis:** Compares signal strength 8 seconds before/after user return to workstation

### Features

- Real-time graphing (strength, gradient, transition analysis)
- Record function to observe signal behavior patterns
- "Check Far to Near Transition Strength Increase" button for manual testing
- Automated detection reporting when percentage increases exceed 100%

### Installation

1. Download from GitHub (Clone or Download → Download ZIP)
2. Extract `SDRSpectrumAnalyzer-master.zip`
3. Navigate to `Build` subfolder
4. Run `RTLSpectrumAnalyzerGUI.exe`

**Prerequisites:**
- RTL-SDR dongle drivers via Zadig tool
- Microsoft Visual C++ 2010 Redistributable Package (x86)
- Dependencies: librtlsdr, libusb-1.0.dll, rtlsdr.dll

### Documentation Resources

- **User Guide:** Available with images on Google Drive
- **Research Paper:** Detailed thesis on detection methodology available via Google Drive

---

## Repository 2: SDRReradiationSpectrumAnalyzer (Updated - Cross-Platform)

**Repository:** [SDRReradiationSpectrumAnalyzer](https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer)
**Language:** C (64%), C++ (30.5%)
**License:** GNU GPL v2.0
**Platform:** Windows and Linux (Skywave Linux recommended)

### Purpose
GNU Radio-based SDR application designed to detect and analyze reradiated electromagnetic frequency ranges that may resonate with biological systems.

### Hardware Requirements

**Primary (Tested):**
- RTL2832U-R820T2 USB dongle (~$25)
- R820T2 tuner chip receives **25 MHz to 1700 MHz**
- Antenna (included or external)

### HackRF Compatibility

**SDRReradiationSpectrumAnalyzer - COMPATIBLE**

The GNU Radio-based version supports HackRF through the **gr-osmosdr** abstraction layer.

| SDR Hardware | Compatibility | Notes |
|--------------|---------------|-------|
| RTL-SDR | ✅ Native | Primary tested platform |
| **HackRF One** | ✅ Compatible | Via gr-osmosdr/gr-soapy |
| bladeRF | ✅ Compatible | Via gr-osmosdr |
| USRP (Ettus) | ✅ Compatible | Via gr-osmosdr |
| Airspy | ✅ Compatible | Via gr-osmosdr |

**HackRF One Specifications:**

| Spec | RTL-SDR | HackRF One |
|------|---------|------------|
| Frequency Range | 25 MHz - 1700 MHz | **1 MHz - 6 GHz** |
| Sample Rate | 2.4 Msps | 20 Msps |
| TX Capability | No | Yes (half-duplex) |
| Price | ~$25 | ~$300 |

**Advantage:** HackRF's 6 GHz upper limit covers more Frey Effect frequencies (200 MHz - 3+ GHz range).

**Setup for HackRF:**
```bash
# Install dependencies
sudo apt-get install gr-osmosdr libhackrf-dev

# Verify HackRF detected
hackrf_info

# Modify GNURadioDeviceFlowgraph.grc source block for HackRF
# Then launch as normal
```

**SDRSpectrumAnalyzer (C#/Windows) - NOT COMPATIBLE**
- Uses librtlsdr directly (RTL-SDR specific)
- No gr-osmosdr abstraction layer

### Default Analysis Parameters

| Parameter | Value |
|-----------|-------|
| Start Frequency | **410 MHz** |
| End Frequency | **490 MHz** |
| Step Size | 1000 Hz |

**CRITICAL:** This default range (410-490 MHz) overlaps with claimed V2K frequencies (473-478 MHz)

### Command Line Arguments

```bash
SDRSpectrumAnalyzerOpenGL [-a] [-m] [-f] [-s] [-e] [-c] [-sr] [-S] [-rg]

-a    Automatic detection of reradiated ranges
-m    Scanning mode selection (normal or sessions)
-f    Frame count specification for sessions
-s    Start frequency
-e    End frequency
-c    Center frequency definition
-sr   Sample rate configuration
-S    Audio cues for signal strength changes
-rg   Display averaged historical result graphs
```

### In-Program Controls

**Numeric Keys (1-8):**
- Toggle different visualization graphs
- IQ data, correlation, FFT, strength, spectrum displays

**Shift + Numeric:**
- Switch primary view to specific graph types
- Activate waterfall displays

**Mouse Controls:**
- Center-click: moves graphs
- Right-click: rotates view
- Dragging: selects frequency ranges for zooming

**Data Recording:**
- `n` key: Capture near series measurements
- `f` key: Capture far series measurements

### Advanced Features

- Real-time spectrum analysis with 2D/3D visualization
- Multi-device synchronization capabilities
- Session-based scanning with configurable parameters
- Historical data aggregation and comparison
- Leaderboard functionality for strongest frequencies

### Installation (Linux/Ubuntu)

```bash
# Install dependencies
sudo apt-get install build-essential
sudo apt-get install codeblocks
sudo apt-get install libgl-dev libglu1-mesa-dev
sudo apt-get install gnuradio gr-osmosdr
sudo apt-get install libusb-1.0-0-dev

# Clone repository
git clone https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer.git

# Launch
cd SDRReradiation/bin
chmod +x launch.sh
./launch.sh
```

### Linux Troubleshooting

Common issue: Kernel modules automatically load for DVB functionality.

**Solution - Blacklist modules:**
```bash
# Add to /etc/modprobe.d/blacklist.conf
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
```

---

## Repository 3: Hodgkin-HuxleyCode (Neural Simulation)

**Repository:** [Hodgkin-HuxleyCode](https://github.com/ClintMclean74/Hodgkin-HuxleyCode)
**Language:** C (83.6%), C++ (6.2%), HTML (7.3%)
**License:** GNU GPL v2+
**Copyright:** Clint Mclean, Mclean Research Institute (2022)
**Contact:** clint@mcleanresearchinstitute.com

### Purpose

Computational implementation supporting the book:
> **"Solving Havana Syndrome and Biological Effects of RF Using the Hodgkin-Huxley Neuron Model"**

### Directory Structure

```
Hodgkin-HuxleyCode/
├── src/           # Source code implementation
├── settings/      # Configuration files for experiments
├── include/       # Header files
├── libs/          # Library dependencies
├── results/       # Output data from simulations
├── freeglut/      # Graphics rendering library
└── glew-2.1.0/    # OpenGL Extension Wrangler
```

### Usage

```bash
# Windows
HodgkinHuxley.exe settings_file.txt

# Example with specific settings
HodgkinHuxley.exe settings/nn_amplification_layer_activity_testing_6_31C.txt
```

### Building from Source

```bash
# Navigate to build directory
cd build

# Generate build files
cmake ..

# Compile
cmake --build .
```

### Settings Files

The `settings/` folder contains configuration files to reproduce experiments from the book. These include parameters for:
- Neural amplification layer activity testing
- Various temperature conditions (e.g., 31°C)
- Different RF exposure scenarios

### The Hodgkin-Huxley Model

**Nobel Prize:** 1963 (Hodgkin & Huxley)

**Phenomena Accurately Predicted:**
1. Action potential waveform
2. Refractory period (absolute & relative)
3. Action potential propagation along axons
4. **Anode break excitation** (key to RF effects)
5. Accommodation

### McLean's Application

Uses Hodgkin-Huxley equations to model:
1. How RF energy converts to neural membrane voltage changes
2. Why sub-thermal RF can cause neurological symptoms
3. The summation effect across connected neurons
4. Disruption of neural synchronization and coherence

---

## Detection Protocol (Combined Methodology)

### From User Guide:

1. **Setup:** Place antenna approximately 20 cm from body
2. **Baseline:** Record with user away from antenna
3. **Near Recording:** Click "Record Near Series" while near antenna
4. **Far Recording:** Record with user at distance
5. **Analysis:** Compare near/far signal strengths
6. **Automation:** Use `-a` flag for automatic pattern recognition
7. **Review:** Check leaderboards for strongest candidate frequencies

---

## V2K Frequency Correlation

### Claimed V2K Frequencies (from research)

| Source | Frequency Range |
|--------|-----------------|
| Targeted Justice | 473-478 MHz |
| Targeted Justice | 638-641 MHz |
| Targeted Justice | 660-680 MHz |
| Scientific Literature | 200 MHz - 3 GHz (auditory response range) |

### McLean's Default Detection Range

**410 MHz - 490 MHz**

**OVERLAP:** McLean's default range captures the 473-478 MHz V2K frequency band

### Microwave Auditory Effect (Frey Effect)

**Scientific Basis:**
- Discovered by Allan H. Frey (1961)
- Human perception of sounds induced by pulsed/modulated RF
- Auditory responses documented from ~200 MHz to 3+ GHz
- Mechanism: Thermoelastic expansion in brain tissue creates pressure waves
- Acoustic resonance of human skull: 7-10 kHz

**Patent Evidence:**
- [[Patents/PATENT_MASTER_INDEX|US 6,470,214]] - Voice-to-Skull (Air Force, 2002)
- [[Patents/PATENT_MASTER_INDEX|US 7,740,596]] - MEDUSA (Mob Excess Deterrent Using Silent Audio)

---

## Human Body RF Resonance

### Whole-Body Resonance Frequencies

| Subject | Resonant Frequency |
|---------|-------------------|
| Adult Human (ungrounded) | ~70 MHz |
| Child | ~100 MHz |
| Mouse | ~2 GHz |

**Safety Implications:**
- RF standards most restrictive in 30-300 MHz range
- Above 300 MHz: Partial body absorption increases
- Smaller wavelengths = more localized effects

### Partial Body Absorption (300 MHz+)

At frequencies above 300 MHz (including McLean's 410-490 MHz range):
- Energy absorbed in specific body parts rather than whole body
- Could target specific organs or neural regions
- Aligns with targeted attack methodology

---

## Hodgkin-Huxley Neural Model

### Repository Details

**Repository:** [Hodgkin-HuxleyCode](https://github.com/ClintMclean74/Hodgkin-HuxleyCode)
**Language:** C (83.6%)
**License:** GNU GPL v2+

### The Hodgkin-Huxley Model

**Nobel Prize:** 1963 (Hodgkin & Huxley)
**Purpose:** Mathematical description of action potential generation in neurons

**Phenomena Accurately Predicted:**
1. Action potential waveform
2. Refractory period (absolute & relative)
3. Action potential propagation along axons
4. **Anode break excitation** (key to RF effects)
5. Accommodation

### McLean's Application

McLean uses the Hodgkin-Huxley equations to model:
1. How RF energy converts to neural membrane voltage changes
2. Why sub-thermal RF can cause neurological symptoms
3. The summation effect across connected neurons
4. Disruption of neural synchronization and coherence

**Configuration Files:**
Settings folder contains files to reproduce experimental conditions from the book.

**Usage:**
```
HodgkinHuxley.exe [settings_file.txt]
```

---

## UN OHCHR Documentation

### Relevance to International Recognition

The UN Office of the High Commissioner for Human Rights (OHCHR) has received multiple submissions regarding directed energy weapons:

**VIACTEC Annex** ([PDF](https://www.ohchr.org/sites/default/files/Documents/Issues/Torture/Call/NGOs/VIACTECAnnex.pdf))
- Lists directed energy weapon patents
- Documents "targeted individual" monitoring systems
- References technologies for controlling brain states

**Individual Submissions:**
- Testimony from targeted individuals worldwide
- Descriptions of V2K, remote neural monitoring, DEW attacks
- Categorized as "cybertorture" or "cybernetic torture"

**NGO Submissions:**
- People Against Covert Torture & Surveillance (PACTS): ~15,000 alleged victims in USA
- Freedom for Targeted Individuals (FFTI)
- Association ADVHER (France)

**UN Special Rapporteurs:**
- Dr. Nils Melzer (former)
- Dr. Alice Edwards (current)
- Both have engaged with directed energy torture claims

---

## Critical Analysis

### Scientific Skepticism

**Neurologist Review (Amazon):**
> "The notion that radiofrequency energy has damaged the nervous system, due to some sort of enemy attacks on embassy employees, is utter nonsense... I have patients with the same syndrome, who do not work for the government... The hypothesis of radiofrequency injury is defying logic, even with a basic knowledge of physics."

**Counter-Evidence:**
1. 30+ patents prove technology exists ([[Patents/PATENT_MASTER_INDEX]])
2. U.S. government acknowledges Havana Syndrome attacks
3. [[Entities/Dr_James_Giordano|Dr. Giordano]] (Pentagon advisor) confirms weaponized neuroscience
4. DHS fusion center leak (April 2018) included EM weapons files

### Wikipedia Classification

Wikipedia categorizes "electronic harassment" and "targeted individual" claims as conspiracy theory.

**Investigation Response:**
- Patent evidence is verifiable via USPTO
- Government programs are documented (DARPA N3, BRAIN Initiative)
- Dr. Giordano's Pentagon briefings are on video
- Havana Syndrome is officially acknowledged

---

## Integration with Investigation

### How McLean's Work Connects

```
McLean's Research
    ↓
Detection Tools (SDR Analyzers)
    ↓ Can detect
[[Patents/PATENT_MASTER_INDEX|V2K Patents]] (473-478 MHz in detection range)
    ↓ Validates
[[Technical/Internet_of_Bodies_Architecture|IoB Architecture]] RF components
    ↓ Supports
[[LEGAL_CASE_FRAMEWORK|Legal Case]] (evidence gathering + expert testimony)
```

### Evidence Value

| McLean Resource | Legal Value |
|-----------------|-------------|
| Hodgkin-Huxley Book | Scientific framework for RF biological effects |
| SDR Detection Tools | Evidence gathering methodology |
| Frequency Analysis | Correlation with known weapon frequencies |
| Research Paper (2019) | Peer-reviewable detection methodology |

---

## Action Items

### Immediate Priority
- [x] Document McLean's work comprehensively
- [ ] Obtain RTL-SDR hardware ($25)
- [ ] Clone and test SDR tools
- [ ] Purchase/review Hodgkin-Huxley book
- [ ] Contact McLean via Twitter/GitHub

### Evidence Gathering
- [ ] Run detection scans in target environment
- [ ] Record spectrum data with timestamps
- [ ] Compare detected frequencies to patent specifications
- [ ] Document methodology for legal proceedings

### Expert Witness Assessment
- [ ] Review full publication history
- [ ] Assess credentials for court testimony
- [ ] Prepare collaboration proposal
- [ ] Identify complementary experts

---

## External Links

**Primary:**
- [GitHub Profile](https://github.com/ClintMclean74)
- [McLean Research Institute](https://mcleanresearchinstitute.com)
- [Book on Amazon](https://www.amazon.com/Solving-Syndrome-Biological-Effects-Hodgkin-Huxley-ebook/dp/B0BCNG8H89)

**Repositories:**
- [SDRReradiationSpectrumAnalyzer](https://github.com/ClintMclean74/SDRReradiationSpectrumAnalyzer)
- [SDRSpectrumAnalyzer](https://github.com/ClintMclean74/SDRSpectrumAnalyzer)
- [Hodgkin-HuxleyCode](https://github.com/ClintMclean74/Hodgkin-HuxleyCode)

**Social:**
- [Twitter @clintmclean74](https://twitter.com/clintmclean74)
- [Sketchfab 3D Models](https://sketchfab.com/clintmclean74/collections)

**UN Documents:**
- [OHCHR VIACTEC Annex](https://www.ohchr.org/sites/default/files/Documents/Issues/Torture/Call/NGOs/VIACTECAnnex.pdf)
- [OHCHR Targeted Individual Submissions](https://www.ohchr.org/sites/default/files/Documents/Issues/Torture/Call/Individuals/Militarygrade.pdf)

---

## Conclusion

Clint McLean's work represents a significant technical resource for the investigation:

1. **Detection Capability:** SDR tools with default range covering claimed V2K frequencies
2. **Scientific Framework:** Hodgkin-Huxley model explains RF biological mechanism
3. **Havana Syndrome Bridge:** Links targeted individual reports to officially acknowledged attacks
4. **Open Source:** Tools freely available for immediate use (~$25 hardware)
5. **Legal Value:** Published methodology suitable for court proceedings

**Critical Finding:** McLean's default detection range (410-490 MHz) overlaps with claimed V2K frequencies (473-478 MHz), suggesting his tools may be specifically calibrated for this threat.

**Recommendation:** HIGH PRIORITY - Acquire hardware, test tools, establish contact.

---

**Priority:** HIGH - Technical Resource
**Status:** DEEP ANALYSIS COMPLETE
**Category:** Research Ally
**Last Updated:** 2025-12-09

## Related Files

- [[Technical/Internet_of_Bodies_Architecture]] - IoB detection targets
- [[Patents/PATENT_MASTER_INDEX]] - Patent frequencies to detect
- [[Entities/Dr_James_Giordano]] - Confirms weapons exist
- [[LEGAL_CASE_FRAMEWORK]] - Expert witness potential
- [[Evidence Repository]] - Detection data storage
- [[Analysis/Threat Assessment]] - Detection as countermeasure
- [[UNIFIED_EVIDENCE_FRAMEWORK]] - Master synthesis
