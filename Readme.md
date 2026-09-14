# Physics-Informed AI Benchmarking

## Project Overview
This project explores the intersection of classical mechanics and deep learning. It consists of a custom-built 2D physics engine that generates synthetic collision data, and a PyTorch deep learning pipeline designed to predict post-collision velocities. The final phase benchmarks whether a standard Multi-Layer Perceptron (MLP) can independently discover the Law of Conservation of Momentum.

## File Architecture
* **`main.py`**: The 2D physics engine. Simulates elastic collisions, gravity, and friction, and generates `physics_data.csv`.
* **`eda.py`**: Validates the synthetic data by calculating total system momentum to ensure no data leaks or mathematical engine bugs exist.
* **`ml_pipeline.py`**: Preprocesses data (StandardScaler) and establishes baseline MSE scores using Scikit-Learn (Linear Regression & Random Forest).
* **`pytorch_model.py`**: Defines, trains, and saves the Neural Network architecture (PhysicsNet) to handle non-linear collision algebra.
* **`benchmark.py`**: Evaluates the trained model's predictions against the Conservation of Momentum formula.

## Key Findings
While the deep learning model achieved high accuracy in predicting final velocities (MSE: 1.38), it failed to conserve total system momentum (Average Momentum Error: ~3,000). This demonstrates that while standard MLPs excel at approximating continuous functions, they do not inherently deduce underlying physical laws, highlighting the necessity for Physics-Informed Neural Networks (PINNs) in scientific machine learning.

## Tech Stack
* Python 3.x
* PyTorch (Deep Learning)
* Scikit-Learn (Baselines & Preprocessing)
* Pandas & NumPy (Data Manipulation)
