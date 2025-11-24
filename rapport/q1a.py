from pathlib import Path
import pennylane as qml
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

IMAGE_OUTPUT_FORMAT = "mpl"
IMAGES_FOLDER = "images"

def draw_circuit(qc: QuantumCircuit) -> None:
    output_path = Path(IMAGES_FOLDER, "circuit_q1a.jpg")
    qc.draw(output=IMAGE_OUTPUT_FORMAT, filename=output_path, fold=-1)
    print("generated circuit in", output_path)


def create() -> QuantumCircuit:
    x_qubits: QuantumRegister = QuantumRegister(2, name='x')
    a_qubit: QuantumRegister = QuantumRegister(1, name='a')

    # On définit les qubits du circuit
    qc = QuantumCircuit(x_qubits, a_qubit)

    c_nots = [[0,2], [1,2]]
    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    return qc

qc : QuantumCircuit = create()
draw_circuit(qc)