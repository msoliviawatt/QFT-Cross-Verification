import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
from getpass import getpass


def R(angle, qubit):
    qml.PhaseShift(angle, qubit)

def qft_control_rotate(control: int, target: int, k: int):
    expo = -2 * np.pi / (1 << k)
    qml.ctrl(R, control = control)(expo, target)

def qft_trapped_ion(n: int, config: list[list[int]], shots=1024) -> map:
    # Initilize a new device
    dev = qml.device('ionq.simulator', api_key="MXzNBT3ZB0Xuiu6onAmXGaSqGCclASYq", wires=n, shots=shots)
    
    # We must assign the initial circuit function to every unique circuit created
    @qml.qnode(dev)
    def circuit():
        cnt = n

        for i in range(n):
            if config[i] == 1:
                qml.X(i)

        for qubit in range(cnt):
            qml.Hadamard(wires=qubit)
            for control in range(qubit + 1, cnt):
                k = control - qubit + 1
                qft_control_rotate(control, qubit, k)

        return qml.counts()

    result = circuit()

    fig, ax = qml.draw_mpl(circuit, style='pennylane', decimals=2)()

    return result

# Testing
# result = qft_trapped_ion(2, [1, 0], 1024)
# print(result)

# result = qft_trapped_ion(5, [1, 0, 1, 1, 1], 1024)
# print(result)