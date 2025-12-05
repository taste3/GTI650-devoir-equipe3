from pathlib import Path
import pennylane as qml
from qiskit import transpile
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector, partial_trace

IMAGES_FOLDER = "images"

def draw_circuit(qc: QuantumCircuit) -> None:
    output_path = Path(IMAGES_FOLDER, "circuit_grover_sudoku2x2.jpg")
    # L'argument fold=-1 permet de générer l'image du circuit en une seule ligne
    #qc.draw(output=IMAGE_OUTPUT_FORMAT, filename=output_path, fold=-1)
    qc.draw(output="mpl", filename=output_path)
    print("Une image du circuit à été généré à ", output_path)

def show_probabilities(qc: QuantumCircuit):
    output_path = Path(IMAGES_FOLDER, "probabilites_sudoku2x2.jpg")
    # on doit retirer les mesures pour éviter une erreur 'Cannot apply instruction with classical bits: measure'
    qc_sans_mesures = qc.remove_final_measurements(inplace=False)
    matrice_densite = Statevector.from_instruction(qc_sans_mesures)

    reduced = partial_trace(matrice_densite, [4, 5, 6, 7, 8])
    probabilites = np.real(np.diag(reduced.data))

    # On formate attribues les probabilités à leurs vecteur d'états associé (ex: 7 = 0111)
    probabilites = {format(i, "04b"): probabilites[i] for i in range(16)}

    plot_histogram(probabilites, figsize=(10,7), title="Probabilités de mesures", filename=output_path)
    print("Un histogramme illustrant les probabilités de résultat à été généré à ", output_path)


def compter_cnot(qc : QuantumCircuit):
    # J'ai essayé d'utiliser les fonctions de pennylane, mais puisque mon circuit est en qiskit j'ai décidé d'explorer le SDK Qiskit
    # Qiskit donne une fonction qui permet de décomposer le circuit en rotations (u3) et en portes CNOT (cx) 
    # https://quantum.cloud.ibm.com/docs/en/api/qiskit/transpiler
    qc_transpile = transpile(qc, basis_gates=["u3", "cx"], optimization_level=0)
    
    #Si on veut voir le circuit réel
    #draw_circuit(qc_transpile)

    #count_ops permet de compter le nombre de chaque type de portes
    # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.QuantumCircuit
    nbre_cnots = qc_transpile.count_ops().get("cx", 0)

    print(f"Ce circuit équivaut à {nbre_cnots} portes CNOT")

def find_optimal_n_iterations():
    # nous avons un sudoku 2x2
    taille_sudoku = 2
    print(f"Pour un sudoku n={taille_sudoku} ({taille_sudoku}x{taille_sudoku})")
    
    nbre_grilles_possibles = taille_sudoku**(taille_sudoku*taille_sudoku)
    print(f"Il y a N={nbre_grilles_possibles} combinaisons possibles")

    theta = np.arcsin(1/np.sqrt(nbre_grilles_possibles))
    print(f"Nous avons un theta = {theta} rad")

    # On isole k dans la formule (2k+1)*theta = pi/2
    k = (np.pi-2*theta)/(4*theta)
    nbre_iterations = int(np.round(k))
    print(f"Ce qui nous donne un k={k}")
    print(f"On arrondi k pour donner le nombre d'itérations = {nbre_iterations}")

    return (nbre_iterations, k, theta)

def calculer_prob_succes(k, theta):
    prob_succes = np.abs(np.sin((2*k+1)*theta))**2
    print(f"la probabilité de succès est de {prob_succes*100}%")


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
# je ne comprend pas pourquoi 
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

num_iterations, k, theta = find_optimal_n_iterations()
qc : QuantumCircuit = grover(num_iterations)
calculer_prob_succes(k, theta)
compter_cnot(qc)
draw_circuit(qc)
show_probabilities(qc)