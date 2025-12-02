# first install perceval using ```pip install perceval-quandela```
import numpy as np
import matplotlib.pyplot as plt

import perceval as pcvl
import perceval.components as comp
from perceval import Processor, BasicState
from perceval.algorithm import Sampler

# set remote config token
from perceval import RemoteConfig

remote_config = RemoteConfig()

# enter working api key here (replace TOKEN)
remote_config.set_token("TOKEN") 
remote_config.save()

def bitstring_to_fock(bitstring):
    # if the parameter is a string, make it a list of ints
    if isinstance(bitstring, str):
        bits = [int(b) for b in bitstring]
    else:
        bits = list(bitstring)

    n = len(bits)
    N = 2 ** n
    index = int("".join(str(b) for b in bits), 2)

    occ = [0] * N
    occ[index] = 1

    # basic state is fock state w/ perceval
    return BasicState(occ)

# qft matrix
def qft_matrix(num_qubits):
    N = 2 ** num_qubits
    omega = np.exp(2j * np.pi / N)
    matrix = np.array([[omega ** (k * l) for l in range(N)] for k in range (N)], dtype = complex) / np.sqrt(N)

    return pcvl.Matrix(matrix)

# unitary of the qft
def qft_unitary_component(num_qubits):
    U = qft_matrix(num_qubits)
    qft_unit = comp.Unitary(U = U)
    return qft_unit

def qft_photonic(num_qubits: int, config: list[list[int]], shots=1024):

    bitstring = "".join(map(str, config))

    N = 2 ** num_qubits

    qft_unitary = qft_unitary_component(num_qubits)

    processor = Processor("SLOS", qft_unitary)

    input_state = bitstring_to_fock(bitstring)
    processor.with_input(input_state)
    processor.min_detected_photons_filter(1)

    sampler = Sampler(processor)
    results = sampler.sample_count(shots)["results"]

    print("QFT unitary on", N, "modes:")
    pcvl.pdisplay(qft_unitary.U)

    ret = {}

    for key, value in results.items():
        for i in range(len(key)):
            if key[i] == 1:
                ret[format(i, 'b').zfill(num_qubits)] = value 
                break
    ret = dict(sorted(ret.items()))

    return ret

# res_3 = qft_photonic(3, [0, 1, 1], shots = 1024)
# print(res_3)
