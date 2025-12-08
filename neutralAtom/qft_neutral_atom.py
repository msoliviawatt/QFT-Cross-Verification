import math

from bloqade.pyqrack import StackMemorySimulator

from bloqade import qasm2

from typing import Any

import numpy as np
import bloqade.types
from kirin.ir import Method
from bloqade.types import Qubit, MeasurementResult

# Some types we will use, useful for type hints
from kirin.dialects.ilist import IList

from bloqade import squin

Register = IList[Qubit, Any]

@squin.kernel
def hello_world(theta: float) -> IList[MeasurementResult, Any]:
    """
    Prepare a Bell state and measure in a basis that might have a Bell violation
    """
    qubits = squin.qalloc(2)
    squin.h(qubits[0])
    squin.cx(qubits[0], qubits[1])
    squin.rx(theta, qubits[0])
    bits = squin.qubit.measure(qubits)
    return bits


# [kernel].print() prints the raw SSA, which is the intermediate representation of the kernel
# as used internally by Kirin.
hello_world.print()

def GHZ_method_factory(nqubits: int) -> Method:
    @squin.kernel
    def GHZ_state() -> Register:
        qubits = squin.qalloc(nqubits)
        squin.h(qubits[0])
        for i in range(nqubits):
            squin.cx(qubits[i], qubits[i + 1])

        return qubits

    return GHZ_state


kernel = GHZ_method_factory(8)
kernel.print()

import cirq
from bloqade.cirq_utils import emit_circuit, load_circuit

def ghz_prep(nqubits: int) -> cirq.Circuit:
    """
    Builder function that returns a simple N-qubit
    GHZ state preparation circuit
    """
    qubits = cirq.LineQubit.range(nqubits)
    output = cirq.Circuit()
    output.append(cirq.H(qubits[0]))
    for i in range(nqubits - 1):
        output.append(cirq.CX(qubits[i], qubits[i + 1]))
    return output

print(ghz_prep(4))

# Load a cirq circuit into squin
kernel = load_circuit(
    ghz_prep(4),
    kernel_name="ghz_prep_cirq",  # Define the name of the kernel as if one were using @squin.kernel on a function
    register_as_argument=False,  # If the resulting kernel should take in a qubit register (True) or make a new one (False)
    return_register=True,  # If the resulting kernel should return the register of the qubits it acts on.
)

# Then, we can convert the circuit back to cirq.
# Note that this is **not possible** in a general case because
# cirq cannot represent complex control flow.
circuit2: cirq.Circuit = emit_circuit(kernel, ignore_returns=True)
print(circuit2)

import math
from bloqade import qasm2
from bloqade.qasm2 import cu1, h
from bloqade import squin
import matplotlib.pyplot as plt
from collections import Counter

@qasm2.extended
def qft(qreg: qasm2.QReg, n: int):
    for k in range(n):
        h(qreg[k])
        for i in range(k + 1, n):
            cu1(qreg[i], qreg[k], math.pi / 2**(i - k))
    return qreg

@qasm2.extended
def main(n: int):
    q_reg = qasm2.qreg(n)
    c_reg = qasm2.creg(n)

    qft(q_reg, n)

    qasm2.measure(q_reg, c_reg)

    return c_reg


def qft_neutral_atom(n: int, config: list[int], shots=1024):

    sim = StackMemorySimulator(min_qubits=4)
    results = []

    for _ in range(shots):
        output = sim.run(main, [n])
        bitstring = "".join(str(int(bit)) for bit in output)
        results.append(bitstring)
    
    counts = Counter(results)

    sorted_keys = sorted(counts.keys())
    return {k: counts[k] for k in sorted_keys}

def qft_neutral_atom_noisy(n: int, config: list[int], shots=1024):
    # NOTE: This is not yet a NOISY MODEL, NEED TO IMPLEMENt
    sim = StackMemorySimulator(min_qubits=4)
    results = []

    for _ in range(shots):
        output = sim.run(main, [n])
        bitstring = "".join(str(int(bit)) for bit in output)
        results.append(bitstring)
    
    counts = Counter(results)

    sorted_keys = sorted(counts.keys())
    return {k: counts[k] for k in sorted_keys}

# print(qft_neutral_atom(4, [0, 0, 0, 0], 1024))
