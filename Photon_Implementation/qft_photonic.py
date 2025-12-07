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

    #print("QFT unitary on", N, "modes:")
    #pcvl.pdisplay(qft_unitary.U)

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

# set remote config token
from perceval import RemoteProcessor, NoiseModel, RemoteConfig
from perceval.algorithm import Sampler

# put api key here
API_KEY = "_T_eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjE4MCwiZXhwIjoxNzY3NzMxNTU0LjE1ODg3MTR9.EcGJhx6iCNCDP-nt0v8Kjm8odFDlqy79rVjLCOT8kUgvmjfiU12TTn_cOwlDPbK2ViKxEWhqYt4H7el61_BljA"
REMOTE_PLATFORM = "sim:belenos"

remote_config = RemoteConfig()
remote_config.set_token(API_KEY)
remote_config.save()
remote_simulator = RemoteProcessor(REMOTE_PLATFORM) 

def qft_photonic_noisy(num_qubits, bitstring, shots = 1024, platform = REMOTE_PLATFORM, api_key = API_KEY, use_noise=True):
    U = qft_matrix(num_qubits)
    qft_unitary = pcvl.components.Unitary(U)

    # noise model
    noise = None
    if use_noise:
        noise = NoiseModel(transmittance = 0.1, indistinguishability = 0.95, g2 = 0.01)

    processor = RemoteProcessor(platform, api_key, noise = noise)

    try:
        processor.set_circuit(qft_unitary)
    except AttributeError:
        processor.add(0, qft_unitary)

    input_state = bitstring_to_fock(bitstring)
    processor.with_input(input_state)
    processor.min_detected_photons_filter(1)

    sampler = Sampler(processor, max_shots_per_call = shots)
    results = sampler.sample_count(shots)["results"]

    #print("QFT unitary on", num_qubits, "modes:")
    #pcvl.pdisplay(qft_unitary.U)

    ret = {}

    for key, value in results.items():
        for i in range(len(key)):
            if key[i] == 1:
                ret[format(i, 'b').zfill(num_qubits)] = value 
                break
    ret = dict(sorted(ret.items()))

    return ret