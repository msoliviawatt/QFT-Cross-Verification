import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def qft_rotations(circuit, n):
    """
    Qiskit implementation of QFT rotations (Hadamard + Controlled Phase).
    """
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(np.pi/2**(n-qubit), qubit, n)
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    """
    QFT requires swapping qubits at the end to match standard binary ordering.
    """
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft_super_conducting(n: int, config: list[int], shots=1024) -> dict:
    """
    Implements QFT on a Superconducting Quantum Computer Simulator (IBM Qiskit).
    Returns a sorted dictionary with all possible states included.
    """
    
    # 1. Initialize Quantum Circuit
    qc = QuantumCircuit(n)

    # 2. State Preparation
    for i in range(n):
        if config[i] == 1:
            qc.x(i)

    # 3. Apply QFT
    qft_rotations(qc, n)
    swap_registers(qc, n)

    # 4. Measurement
    qc.measure_all()

    # 5. Execution
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator)
    result = simulator.run(transpiled_qc, shots=shots).result()
    raw_counts = result.get_counts()
    
    full_counts = {format(i, f'0{n}b'): 0 for i in range(2**n)}
    
    for bitstring, count in raw_counts.items():
        full_counts[bitstring] = count
        
    sorted_counts = dict(sorted(full_counts.items()))
    
    return sorted_counts