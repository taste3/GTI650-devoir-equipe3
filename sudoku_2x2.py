import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

from sudoku_nxn import calculer_prob_succes, find_optimal_n_iterations, draw_circuit, draw_histogram, compter_cnot


def oracle_sudoku(qc: QuantumCircuit) -> QuantumCircuit:
    c_nots = [[0,4], [1,4], [0,5], [2,5], [1,6], [3,6], [2,7], [3,7]]
    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    # On ajoute le CCCCNOT
    qc.mcx([4,5,6,7], 8)

    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    return qc

#Je me suis basé sur sudoku(2x2).ipynb pour faire ce bout de circuit
# je ne comprend pas comment ça fonctionne 
def inversion_moyenne(qc: QuantumCircuit):
    qubits = [0,1,2,3]
    qc.h(qubits)
    qc.x(qubits)

    qc.h(qubits[3])
    qc.mcx([0,1,2], 3)
    qc.h(qubits[3])
    
    qc.x(qubits)
    qc.h(qubits)

    return qc

def grover(num_iterations) -> QuantumCircuit:
    v_qubits: QuantumRegister = QuantumRegister(4, name='v')
    c_qubits: QuantumRegister = QuantumRegister(4, name='c')
    out_qubit: QuantumRegister = QuantumRegister(1, name='out')
    measures = ClassicalRegister(4, name="m")

    # On définit les qubits du circuit
    qc = QuantumCircuit(v_qubits, c_qubits, out_qubit, measures)

    # On initialise le dernier qubit dans l'état |-> (moins)
    qc.initialize(np.array([1, -1]) / np.sqrt(2), out_qubit)

    # Tour de haddamards sur les 4 premiers qubits
    for i in range(4):
        qc.h(i)

    qc.barrier()

    # On applique l'oracle n fois
    for iteration in range(num_iterations):
        # On applique l'oracle ici (plein de cnots et un CCCNOT)
        qc = oracle_sudoku(qc)
        qc.barrier()
        qc = inversion_moyenne(qc)
        qc.barrier()
        qc.barrier()


    qc.measure(v_qubits, measures)
    return qc

num_iterations, k, theta = find_optimal_n_iterations(taille_sudoku=2)
qc : QuantumCircuit = grover(num_iterations)
calculer_prob_succes(k, theta)
compter_cnot(qc)
draw_circuit(qc, "circuit_grover_sudoku2x2.jpg")
draw_histogram(qc, "probabilites_sudoku2x2.jpg")