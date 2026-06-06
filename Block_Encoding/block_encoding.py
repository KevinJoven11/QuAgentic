import numpy as np

def single_qubit_gate(U, target, n_qubits):

    I = np.eye(2)
    ops = []
    for i in range(n_qubits):
        if i == target:
            ops.append(U)
        else:
            ops.append(I)
    full = ops[0]
    for op in ops[1:]:
        full = np.kron(full, op)
    return full

def Hadamard():
    return (1/np.sqrt(2))*np.array([
        [1, 1],
        [1,-1]
    ], dtype=complex)

def Ry(theta):
    return np.array([
        [np.cos(theta / 2), -np.sin(theta / 2)],
        [np.sin(theta / 2),  np.cos(theta / 2)]
    ], dtype=complex)

def Rx(theta):
    return np.array([
        [np.cos(theta / 2), -1j*np.sin(theta / 2)],
        [-1j*np.sin(theta / 2), np.cos(theta / 2)]
    ], dtype=complex)

def cnot(control, target, n_qubits):

    dim = 2 ** n_qubits
    U = np.zeros((dim, dim))
    for i in range(dim):
        bits = list(map(int, format(i, f"0{n_qubits}b")))
        if bits[control] == 1:
            bits[target] ^= 1
        j = int("".join(map(str, bits)), 2)
        U[j, i] = 1
    return U

def initialize_parameters(num_layers, num_qubits, seed=32):
    rng = np.random.default_rng(seed)
    theta_y = rng.uniform(
        -2*np.pi,
        2*np.pi,
        size=(num_layers, num_qubits)
    )
    theta_x = rng.uniform(
        -2*np.pi,
        2*np.pi,
        size=(num_layers, num_qubits)
    )
    return theta_y, theta_x

def approximate_block_encoding( H, num_layers, theta_y, theta_x):

    num_qubits = int(np.log2(H.shape[0]))
    n_total = num_qubits + 1

    U = np.eye(2**(num_qubits+1))

    for q in range(n_total):
        U = single_qubit_gate( Hadamard(), q, n_total ) @ U

    for layer in range(num_layers):

        for q in range(n_total):
            U = single_qubit_gate(Ry(theta_y[layer][q]), q, n_total) @ U
            U = single_qubit_gate(Rx(theta_x[layer][q]), q, n_total ) @ U 

        for q in range(n_total-1):
            U = cnot(q, q+1, n_total) @ U

    return U