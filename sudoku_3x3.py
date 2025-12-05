from pathlib import Path
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector, partial_trace

from sudoku_nxn import calculer_prob_succes, find_optimal_n_iterations, draw_circuit, IMAGES_FOLDER, compter_cnot

# L'histogramme du 3x3 était pas demandé, mais ça m'aide a valider mon circuit
def draw_histogram(qc: QuantumCircuit, file_name):
    output_path = Path(IMAGES_FOLDER, file_name)
    # on doit retirer les mesures pour éviter une erreur 'Cannot apply instruction with classical bits: measure'
    qc_sans_mesures = qc.remove_final_measurements(inplace=False)
    matrice_densite = Statevector.from_instruction(qc_sans_mesures)

    reduced = partial_trace(matrice_densite, [9,10,11,12,13,14,15])
    probabilites = np.real(np.diag(reduced.data))

    # On formate attribues les probabilités à leurs vecteur d'états associé (ex: 7 = 0111)
    probabilites = {format(i, "04b"): probabilites[i] for i in range(512)}

    plot_histogram(probabilites, figsize=(10,7), title="Probabilités de mesures", filename=output_path)
    print("Un histogramme illustrant les probabilités de résultat à été généré à ", output_path)

def oracle_sudoku(qc: QuantumCircuit) -> QuantumCircuit:
    c_nots = []
    mc_nots = []
    # Contraintes sur les lignes
    c_nots.extend([[0,9], [1,9], [2,9]])    # ligne#1 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([0,1,2], 9)                      # ligne#1 ne doit pas contenir trois 1
    c_nots.extend([[3,10], [4,10], [5,10]]) # ligne#2 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([3,4,5], 10)                     # ligne#2 ne doit pas contenir trois 1
    c_nots.extend([[6,11], [7,11], [8,11]]) # ligne#3 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([6,7,8], 11)                     # ligne#3 ne doit pas contenir trois 1

    # Contraintes sur les colonnes
    c_nots.extend([[0,12], [3,12], [6,12]]) # colonne#1 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([0,3,6], 12)                     # colonne#1 ne doit pas contenir trois 1
    c_nots.extend([[1,13], [4,13], [7,13]]) # colonne#2 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([1,4,7], 13)                     # colonne#2 ne doit pas contenir trois 1
    c_nots.extend([[2,14], [5,14], [8,14]]) # colonne#3 ne doit pas avoir tout des 0 et ne doit pas avoir deux 1
    qc.mcx([2,5,8], 14)                     # colonne#3 ne doit pas contenir trois 1
    
    # On ajoute les c_nots au circuit
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    # On ajoute le CCCCNOT qui vérifie toutes les conditions
    qc.mcx([9,10,11,12,13, 14], 15)

    # On ajoute les c_nots
    for c_not in c_nots:
        qc.cx(c_not[0], c_not[1])

    return qc

#damn ça je sais pas...
def inversion_moyenne(qc: QuantumCircuit):
    qubits = [0,1,2,3,4,5,6,7,8]
    qc.h(qubits)
    qc.x(qubits)

    qc.h(8)
    qc.mcx([0,1,2,3,4,5,6,7], 8)
    qc.h(8)

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
    for iteration in range(num_iterations):
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
draw_circuit(qc, "circuit_grover_sudoku3x3.jpg", fold=76)
draw_histogram(qc, "probabilites_sudoku3x3.jpg")
