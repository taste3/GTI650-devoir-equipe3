from pathlib import Path
import pennylane as qml
import numpy as np
from qiskit import QuantumRegister, QuantumCircuit

IMAGE_OUTPUT_FORMAT = "mpl"
IMAGES_FOLDER = "images"

def draw_circuit(qc: QuantumCircuit) -> None:
    output_path = Path(IMAGES_FOLDER, "circuit-mpl.jpeg")
    qc.draw(output=IMAGE_OUTPUT_FORMAT, filename=output_path)
    print("generated circuit in", output_path)


def create_sudoku_circuit() -> QuantumCircuit:
    v_qubits: QuantumRegister = QuantumRegister(4, name='v')
    c_qubits: QuantumRegister = QuantumRegister(4, name='c')
    out_qubit: QuantumRegister = QuantumRegister(1, name='out')

    # On définit les qubits du circuit
    qc = QuantumCircuit(v_qubits, c_qubits, out_qubit)

    # Tour de haddamards sur les 4 premiers qubits
    for i in range(4):
        qc.h(i)

    # On applique les c_nots
    c_nots = [[0,4], [1,4], [0,5], [2,5], [1,6], [3,6], [2,7], [3,7]]
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    qc.mcx(c_qubits, out_qubit)

    return qc

qc : QuantumCircuit = create_sudoku_circuit()
draw_circuit(qc)