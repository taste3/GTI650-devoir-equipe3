from pathlib import Path
import pennylane as qml
from qiskit import transpile
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector, partial_trace

IMAGES_FOLDER = "images"

def draw_circuit(qc: QuantumCircuit, file_name) -> None:
    output_path = Path(IMAGES_FOLDER, file_name)
    # L'argument fold=-1 permet de générer l'image du circuit en une seule ligne
    #qc.draw(output=IMAGE_OUTPUT_FORMAT, filename=output_path, fold=-1)
    qc.draw(output="mpl", filename=output_path)
    print("Une image du circuit à été généré à ", output_path)

def draw_histogram(qc: QuantumCircuit, file_name):
    output_path = Path(IMAGES_FOLDER, file_name)
    # on doit retirer les mesures pour éviter une erreur 'Cannot apply instruction with classical bits: measure'
    qc_sans_mesures = qc.remove_final_measurements(inplace=False)
    matrice_densite = Statevector.from_instruction(qc_sans_mesures)

    reduced = partial_trace(matrice_densite, [4, 5, 6, 7, 8])
    probabilites = np.real(np.diag(reduced.data))

    # On formate attribues les probabilités à leurs vecteur d'états associé (ex: 7 = 0111)
    probabilites = {format(i, "04b"): probabilites[i] for i in range(16)}

    plot_histogram(probabilites, figsize=(10,7), title="Probabilités de mesures", filename=output_path)
    print("Un histogramme illustrant les probabilités de résultat à été généré à ", output_path)

def calculer_prob_succes(m, theta):
    prob_succes = np.abs(np.sin((2*m+1)*theta))**2
    print(f"La probabilité de succès est de {prob_succes:.4%}")

def find_optimal_n_iterations(n, m):
    # nous avons un sudoku nxn
    print(f"Pour un sudoku n={n} ({n}x{n})")
    
    N = 2**(n*n)
    print(f"Le nombre de combinaisons possibles est N={N}")

    print(f"Le nombre de solutions possibles est m={m}")

    theta = np.arcsin(np.sqrt(m/N))
    print(f"Nous avons un theta={theta:.4}rad")

    # pour trouver le nombre d'itérations k, on isole k dans (2k+1)*theta=pi/2
    k = ((np.pi/2)-theta)/(2*theta)
    print(f"Ce qui nous donne un k={k}")
    k = int(np.round(k))
    print(f"On arrondi k pour donner le nombre d'itérations k={k}")

    return (k, theta)


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