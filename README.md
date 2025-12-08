# Quantum Fourier Transform Cross-Verification
Simulations and interference/noise comparisions of the Quantum Fourier Transform on various quantum devices

## Team
Olivia Watt
Thuan Van Tu
Brenden Jeffryes
Hoon Sung

## Introduction
This project tests and compares performance of the **Quantum Fourier Transform (QFT)** algorithm across four different quantum computing platforms:

**Quandela's Perceval Framework for Photonic Quantum Computing**
- Uses SLOS (strong linear optical simulation) algorithm
- Allows for both local and remote cloud simulations with a valid token
- Produces results as Fock states that can be converted to bitstrings

**PennyLane for Quantum Computing with Trapped Ions**
- add text here
- add text here

**IBM Qiskit for Superconducting Quantum Computers**
- add text here
- add text here

**QuEra's Bloqade SDK for Neutral Atom Quantum Computing**
- add text here
- add text here

## How to Use This Repository

## Experiments

## Notes
Since the purpose of the Quantum Fourier Transform is to apply a phase to each qubit of a created superposition state, measuring in the computational basis does not yield very useful information. The expected results are an equal probability distribution across all bitstrings. To improve this experiment, it could be worthwhile to integrate the QFT unitary into the Phase Estimation Algorithm to see how results may vary -- or to run a different algorithm/process altogether.


## References
### General
- https://journals.aps.org/prx/pdf/10.1103/PhysRevX.11.031049
- https://pennylane.ai/qml/demos/tutorial_qft#defining-the-quantum-fourier-transform

### Photonic/Optical Quantum Computing
- https://arxiv.org/abs/quant-ph/0512071
- https://arxiv.org/abs/2404.03367
- https://strawberryfields.ai/photonics/
- https://perceval.quandela.net/docs/v1.1/index.html

### Quantum Trapped-Ion Computing
- https://docs.ionq.com/
- https://www.quera.com/glossary/trapped-ions
- https://arxiv.org/pdf/2404.11572
