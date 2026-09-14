Physics-Informed AI Benchmarking for Collision Dynamics

A small scientific machine learning project that investigates whether neural
networks can accurately predict collision dynamics while also respecting
physical constraints such as conservation of momentum.

Motivation

Neural networks are powerful function approximators, but predictive accuracy
does not automatically guarantee that their predictions obey the physical laws
of the system that generated the data.

This project explores that gap using a custom 2D collision simulator.

The main question is:

Can a conventional neural network predict post-collision velocities accurately
without explicitly enforcing the underlying physical constraints?

The project also provides a foundation for comparing an unconstrained neural
network with a physics-informed training objective.

Project Overview

The project contains five main stages:

Physics simulation — generate synthetic collision data using a custom 2D
physics engine.

Data validation — verify that the simulator behaves consistently with the
intended physical assumptions.

ML baselines — compare Linear Regression and Random Forest models.

Neural network — train a PyTorch MLP to predict post-collision velocities.

Physics benchmarking — evaluate predictions not only by velocity error but
also by their physical consistency.

The intended final extension is a physics-informed MLP that adds a conservation
of momentum penalty to the ordinary prediction loss.

Project Architecture

                Custom 2D Physics Engine
                         |
                         v
                 Synthetic Collision Data
                         |
              +----------+----------+
              |                     |
              v                     v
         Data Validation           EDA
              |
              v
       +------+------+------+
       |             |      |
       v             v      v
    Linear        Random   Standard
   Regression     Forest     MLP
                            |
                            v
                    Physics Benchmark
                            |
                            v
                 Physics-Informed MLP
                            |
                            v
                   Model Comparison

Repository Structure

File

Purpose

main.py

Generates synthetic collision data using the 2D physics engine

eda.py

Performs basic physical/data validation

ml_pipeline.py

Preprocessing and classical ML baselines

pytorch_model.py

Defines and trains the PyTorch neural network

benchmark.py

Evaluates predictions against physical quantities

data.csv

Generated collision dataset

Physics Engine

The simulator models 2D collisions between objects with variable physical
parameters.

The generated samples include quantities such as:

Object masses

Object radii

Initial positions

Initial velocities

Collision parameters

Coefficient of restitution

Other simulation parameters

The collision response is calculated from the geometry and relative motion of
the colliding objects.

Mass Assumption

The simulator uses:

mass = pi * radius^2

This is treated as a simplified 2D model in which objects are uniform discs with
constant areal density, so mass is proportional to area.

This is a modelling assumption for the simulation rather than a universal
physical statement about mass.

Dataset

The simulator is used to generate a large synthetic dataset of collision events.

The dataset is designed to provide controlled inputs and corresponding
post-collision velocity targets for supervised learning.

The model can therefore be evaluated against both:

The simulated ground-truth velocities

Physical quantities reconstructed from the predictions

This separation is important because a model can have good prediction error
while still violating a physical invariant.

Machine Learning Baselines

Two classical models are used as baselines:

Linear Regression

Provides a simple linear reference point.

Random Forest

Provides a nonlinear tree-based reference model.

These baselines help determine whether the collision mapping requires nonlinear
function approximation and whether the neural network provides an advantage
over conventional ML methods.

Neural Network

The baseline neural network is a fully connected MLP implemented using PyTorch.

Conceptually:

Input Features
      |
      v
   Dense Layer
      |
     ReLU
      |
      v
   Dense Layer
      |
     ReLU
      |
      v
 Output Velocities

The model is trained using Mean Squared Error (MSE) between predicted and
simulated post-collision velocities.

The input features are standardized using a scaler fitted only on the training
data to avoid data leakage.

Physics Benchmark

Prediction accuracy alone is not sufficient for this experiment.

For an isolated collision system, total linear momentum should be conserved:

initial momentum ≈ final momentum

For two objects, momentum is evaluated component-wise:

p_x = m1*v1_x + m2*v2_x
p_y = m1*v1_y + m2*v2_y

The benchmark compares momentum calculated from the initial conditions with
momentum calculated using the model's predicted final velocities.

This allows the project to measure the difference between:

Statistical accuracy — how close predicted velocities are to the targets

Physical consistency — how closely predictions satisfy the conservation
constraint

Current Result

The baseline MLP achieves a velocity prediction MSE of approximately:

MSE ≈ 1.38

However, the current benchmark reports a much larger absolute momentum error.

This result is interpreted carefully:

A conventional MLP can achieve useful predictive accuracy without explicitly
being constrained to preserve the physical invariants of the system.

The magnitude of momentum error should be interpreted relative to the momentum
scale of the dataset. Future evaluation should therefore report normalized or
relative momentum error in addition to absolute error.

Physics-Informed Extension

The main planned extension is to train a second model using a physics-aware
objective.

A conventional model minimizes:

L_data = MSE(predicted velocity, true velocity)

A physics-informed model can use:

L_total = L_data + lambda * L_momentum

where L_momentum penalizes disagreement between initial and predicted final
momentum.

This creates a controlled comparison:

             Standard MLP
                  |
                  v
          Prediction accuracy
                  |
                  v
            Physics error


        Physics-Informed MLP
                  |
                  v
       Prediction + physics loss
                  |
                  v
            Physics error

The purpose is not to assume beforehand that the physics-informed model will be
better, but to experimentally measure the tradeoff between prediction accuracy
and physical consistency.

Evaluation

The project should report multiple metrics rather than relying on one number.

Prediction Metrics

Mean Squared Error (MSE)

Mean Absolute Error (MAE)

Per-output error

Physics Metrics

Mean absolute momentum error

Median momentum error

Standard deviation

95th percentile error

Relative momentum error

A useful normalized measure is:

relative error =
|p_predicted - p_true| / (|p_true| + epsilon)

Reporting relative error is important because absolute momentum values depend on
the scale of the masses and velocities in the dataset.

Generalization Experiments

A future version of the project will test whether the models generalize outside
their training distribution.

For example:

Training radius: 10–40
Testing radius: 40–50

Similar experiments can be performed by holding out ranges of:

Mass

Velocity

Radius

Collision parameters

This allows comparison of standard and physics-informed models under
out-of-distribution conditions.

Important Physics Consideration

Momentum conservation should be evaluated carefully.

The tracked objects form an isolated system only when external forces do not
transfer momentum to or from the system being measured.

Because the simulator can include effects such as gravity and friction, the
project should distinguish between:

Isolated collision experiment

Used to test conservation of momentum.

External-force experiment

Used to study how the model predicts dynamics when forces act on the system.

This distinction prevents an incorrect assumption that momentum must always remain
constant in every simulation configuration.

Visualizations

Recommended plots for the project include:

Initial momentum vs final momentum

Momentum error distribution

True velocity vs predicted velocity

Prediction residual distribution

Prediction error vs mass

Prediction error under different collision conditions

Standard MLP vs physics-informed MLP comparison

These plots make the results easier to interpret and make the project more useful
as a portfolio/research artifact.

Reproducibility

The project is intended to be reproducible from the source code.

A polished version should document:

Python version

Required packages

Dataset generation command

Training command

Benchmark command

Random seeds

Model hyperparameters

Example workflow:

python main.py
python eda.py
python ml_pipeline.py
python pytorch_model.py
python benchmark.py

Adjust the commands above if the scripts require additional arguments.

Limitations

This project uses a simplified physics simulation rather than a complete
high-fidelity physics engine.

Important limitations include:

Simplified 2D assumptions

Synthetic rather than real-world data

Limited model architectures

Dependence on the simulator's assumptions

A conventional MLP does not explicitly encode physical laws

Absolute momentum error depends on the scale of the simulated system

These limitations are part of the motivation for investigating physics-informed
objectives rather than being hidden from the evaluation.

Future Work

Possible extensions include:

Physics-informed loss functions

Out-of-distribution testing

Larger hyperparameter studies

More detailed conservation metrics

Energy conservation analysis

Angular momentum analysis

Additional collision scenarios

Better visualization and experiment tracking

Comparison with other physics-aware architectures

Why This Project?

The goal is not simply to achieve the lowest prediction error.

The project investigates a broader scientific ML question:

Is statistical prediction accuracy enough when the model is expected to
represent a physical system?

By comparing conventional and physics-constrained learning objectives, the project
aims to demonstrate the difference between fitting observed data and respecting
the structure of the underlying system.

Tech Stack

Python 3.x

PyTorch

Scikit-learn

NumPy

Pandas

Matplotlib

Author

Built as a second-year AIML project exploring the intersection of classical
mechanics and deep learning.
