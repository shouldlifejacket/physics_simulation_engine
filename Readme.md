Physics Simulation Engine + ML Benchmark

A small project where I built a 2D physics simulation, generated collision data
from it, and then used machine learning models to predict the velocities after
a collision.

The main thing I wanted to test was whether a normal neural network would learn
the physics well enough on its own, or whether it could make accurate predictions
while still breaking a physical rule like conservation of momentum.

What the project does

The project has five main parts:

Generate collision data using a custom 2D physics engine.

Check the generated data and the physics calculations.

Train a few standard ML models as baselines.

Train a PyTorch MLP to predict the final velocities.

Compare the model's predictions with the actual momentum of the system.

The current version mainly focuses on the standard MLP. A physics-informed version
is planned as the next step.

Files

File

What it does

main.py

Runs the physics simulation and generates the dataset

eda.py

Checks the generated data and momentum calculations

ml_pipeline.py

Runs the Scikit-learn baseline models

pytorch_model.py

Defines and trains the PyTorch MLP

benchmark.py

Checks the trained model against the momentum calculation

data.csv

Generated collision data

Physics Simulation

The simulator is a simplified 2D physics engine. It generates collisions between
two objects with different positions, velocities, radii and other parameters.

The collision response is calculated from the relative position and velocity of
the objects.

For the 2D objects in this simulation, I use:

mass = pi * radius^2

This is a simplified assumption where the objects are treated as uniform 2D discs
with constant density. It is mainly used to give the simulation objects different
masses based on their size.

The simulator also contains things like gravity and friction. Because of that,
momentum conservation is only used as a benchmark for cases where the tracked
system can be treated as isolated.

Dataset

The simulation is used to generate thousands of collision examples.

The inputs contain information about the two objects and their initial state,
while the targets are their velocities after the collision.

The idea is to create data where the correct answer is produced by the physics
simulation instead of manually collecting real-world measurements.

ML Models

I currently compare three approaches:

Linear Regression

Used as a simple baseline to see how much of the collision relationship can be
approximated with a linear model.

Random Forest

Used as a nonlinear classical ML baseline.

PyTorch MLP

A fully connected neural network is used to predict the post-collision velocities.

The current network is roughly:

Input
  |
64 neurons
  |
ReLU
  |
64 neurons
  |
ReLU
  |
Output

The model is trained using MSE loss.

The input features are standardized before training.

Current Results

The MLP currently gets a velocity prediction MSE of around:

1.38

However, when the predicted velocities are used to calculate the final momentum,
the error is much larger (around 3000 in the current benchmark).

This is the interesting part of the project.

A model can be reasonably good at predicting the values it was trained on without
necessarily being forced to obey the physical relationships between those values.

The momentum benchmark is therefore separate from the normal prediction loss.

Momentum Check

For two objects, the total linear momentum is calculated as:

p_x = m1 * v1_x + m2 * v2_x
p_y = m1 * v1_y + m2 * v2_y

For an isolated collision:

initial momentum ≈ final momentum

The benchmark compares the initial momentum with the momentum obtained from the
model's predicted final velocities.

One improvement I want to make is to report relative momentum error as well as
absolute error, since the absolute value depends on the scale of the masses and
velocities in the dataset.

Planned Physics-Informed Model

The next version will add a physics-based term to the neural network's loss.

The normal model uses something like:

loss = velocity MSE

The physics-informed version will use:

loss = velocity MSE + lambda * momentum loss

The goal is to compare the two models and see whether explicitly including the
momentum constraint reduces the physics error.

I don't want to assume beforehand that the physics-informed model will always be
better. The point is to measure the difference.

Planned Experiments

Some of the experiments I want to add are:

Compare standard MLP vs physics-informed MLP

Report MAE as well as MSE

Report absolute and relative momentum error

Plot predicted vs actual velocities

Plot initial vs final momentum

Plot the distribution of momentum errors

Test the models on data outside the training range

Check how the physics loss affects normal prediction accuracy

For example, an out-of-distribution test could train the model on one range of
radii and then test it on a higher range that it did not see during training.

Important Limitation

This is a simplified physics simulation, not a full physics engine.

The results also depend on the assumptions made by the simulator. In particular,
gravity and friction need to be handled carefully when testing momentum
conservation because they can introduce external forces.

The purpose of the project is mainly to experiment with the relationship between
machine learning predictions and known physical constraints.

Running the Project

Install the required Python packages first.

For example:

pip install numpy pandas matplotlib scikit-learn torch

Then the general workflow is:

python main.py
python eda.py
python ml_pipeline.py
python pytorch_model.py
python benchmark.py

The exact commands may change as more experiments are added.

Tech Used

Python

PyTorch

Scikit-learn

NumPy

Pandas

Matplotlib

Why I Made This

I wanted to try something beyond a normal ML prediction project.

Instead of only asking whether a model gets a low MSE, I wanted to check whether
the predictions still make sense from a physics point of view.

The project is still a work in progress, and the main thing I want to explore next
is whether adding the physical constraint directly to the training process makes
the model more physically consistent.
