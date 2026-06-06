import numpy as np
from scipy.optimize import minimize
import os

os.makedirs(
    "experiments",
    exist_ok=True
)

# importa tus funciones
from block_encoding import (
    approximate_block_encoding
)

from database import (
    initialize_database,
    save_experiment,
    show_experiments
)

def extract_block(U, H):
    d = H.shape[0]
    return U[:d, :d]

def normalize_hamiltonian(H):
    alpha = np.linalg.norm(H, ord=2)
    return H / alpha, alpha

def cost_function(U, H):
    H_norm, alpha = normalize_hamiltonian(H)
    A = extract_block(U, H)
    return np.linalg.norm(A - H_norm)

def unpack_params(params, num_layers, n_total):
    N = num_layers*n_total
    theta_y = params[:N].reshape( num_layers, n_total )
    theta_x = params[N:].reshape( num_layers, n_total )
    return theta_y, theta_x

def objective(params, H, num_layers):

    n_system = int(np.log2(H.shape[0]))
    n_total = n_system + 1
    theta_y, theta_x = unpack_params( params, num_layers, n_total )
    U = approximate_block_encoding( H, num_layers, theta_y, theta_x )
    return cost_function( U, H )

def load_matrix(path):
    return np.load(path)

def extract_block(U, H):
    d = H.shape[0]
    return U[:d,:d]

if __name__ == "__main__":

    initialize_database()

    H = load_matrix("matrix.npy")

    print("Input matrix:")
    print(H)

    num_layers = 5

    num_qubits = int(np.log2(H.shape[0]))
    n_total = num_qubits + 1

    num_params = 2 * num_layers * n_total

    rng = np.random.default_rng(32)

    x0 = rng.uniform(
        0,
        2*np.pi,
        size=num_params
    )

    result = minimize(
        objective,
        x0,
        args=(H, num_layers),
        method="Powell"
    )

    print("\nOptimization results")
    print("--------------------")
    print("Initial cost:", objective(x0, H, num_layers))
    print("Final cost:", result.fun)

    # Recover optimized parameters
    theta_y_opt, theta_x_opt = unpack_params(
        result.x,
        num_layers,
        n_total
    )

    # Build optimized circuit
    U_opt = approximate_block_encoding(
        H,
        num_layers,
        theta_y_opt,
        theta_x_opt
    )

    # Extract block encoding
    A = extract_block(U_opt, H)

    print("\nBlock Encoding:")
    print(A)


    block_path = (
        f"experiments/block_layers_{num_layers}.npy"
    )

    np.save(
        block_path,
        A
    )

    save_experiment(
        matrix_name="matrix.npy",
        num_layers=num_layers,
        cost=result.fun,
        alpha=1.0,
        num_parameters=num_params,
        theta_y=theta_y_opt,
        theta_x=theta_x_opt,
        block_path=block_path
    )

    print(show_experiments())