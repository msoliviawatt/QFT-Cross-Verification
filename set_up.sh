# Require python >=3.10 installed

# Remove this line and figure out how to set up virtual environment if the command does not work
/usr/bin/python3.11 -m venv .venv


source .venv/bin/activate
pip install bloqade
pip install ipykernel
pip install pennylane
pip install perceval
pip install perceval-quandela
pip install qiskit
pip install qiskit_aer
pip install qiskit_ibm_runtime
pip install pennylane_ionq