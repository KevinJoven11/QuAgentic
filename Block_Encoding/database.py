import sqlite3
import json
from datetime import datetime
import sqlite3
import os

os.makedirs(
    "experiments",
    exist_ok=True
)

def save_experiment(matrix_name, num_layers, cost, alpha, num_parameters, theta_y, theta_x, block_path):
    conn = sqlite3.connect("experiments.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO experiments
        (
            timestamp,
            matrix_name,
            num_layers,
            cost,
            alpha,
            num_parameters,
            theta_y,
            theta_x,
            block_path
        )
        VALUES (?,?,?,?,?,?,?,?,?)
        """,
        (
            datetime.now().isoformat(),
            matrix_name,
            num_layers,
            cost,
            alpha,
            num_parameters,
            json.dumps(theta_y.tolist()),
            json.dumps(theta_x.tolist()),
            block_path
        )
    )

    conn.commit()
    conn.close()

def initialize_database():

    conn = sqlite3.connect("experiments.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        matrix_name TEXT,

        num_layers INTEGER,

        cost REAL,

        alpha REAL,

        num_parameters INTEGER,

        theta_y TEXT,

        theta_x TEXT,

        block_path TEXT

    )
    """)

    conn.commit()
    conn.close()

def show_experiments():

    conn = sqlite3.connect(
        "experiments.db"
    )

    cursor = conn.cursor()

    rows = cursor.execute(
        """
        SELECT
            id,
            timestamp,
            cost,
            num_layers
        FROM experiments
        ORDER BY cost ASC
        """
    ).fetchall()

    conn.close()

    return rows