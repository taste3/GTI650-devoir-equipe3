import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

from sudoku_nxn import calculer_prob_succes, find_optimal_n_iterations, draw_circuit, draw_histogram, compter_cnot

def oracle_sudoku(qc: QuantumCircuit) -> QuantumCircuit:
    c_nots = [[0,9]]
    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    # On ajoute le CCCCNOT qui vérifie toutes les conditions
    qc.mcx([9,10,11,12,13], 14)

    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    return qc

#damn ça je sais pas...
def inversion_moyenne(qc: QuantumCircuit):
    qubits = [0,1,2,3,4,5,6,7,8]
    qc.h(qubits)
    qc.x(qubits)

    #qc.h(qubits[])
    #qc.mcx(qubits[], qubits[])
    #qc.h(qubits[])

    qc.x(qubits)
    qc.h(qubits)

    return qc

def grover(num_iterations) -> QuantumCircuit:
    v_qubits: QuantumRegister = QuantumRegister(9, name='v')
    c_qubits: QuantumRegister = QuantumRegister(6, name='c')
    out_qubit: QuantumRegister = QuantumRegister(1, name='out')
    measures = ClassicalRegister(9, name="m")

    # On définit les qubits du circuit
    qc = QuantumCircuit(v_qubits, c_qubits, out_qubit, measures)

    # On initialise le dernier qubit dans l'état |-> (moins)
    qc.initialize(np.array([1, -1]) / np.sqrt(2), out_qubit)

    # Tour de haddamards sur les 9 premiers qubits
    for i in range(9):
        qc.h(i)

    qc.barrier()

    # On applique l'oracle n fois
    # On applique l'oracle 1 fois pour tester
    for iteration in range(1):
        qc = oracle_sudoku(qc)
        qc.barrier()
        qc = inversion_moyenne(qc)
        qc.barrier()

    qc.measure(v_qubits, measures)
    return qc

k, theta = find_optimal_n_iterations(n=3, m=6)
qc : QuantumCircuit = grover(k)
calculer_prob_succes(k, theta)
compter_cnot(qc)
draw_circuit(qc, "circuit_grover_sudoku3x3.jpg")
draw_histogram(qc, "probabilites_sudoku3x3.jpg")
