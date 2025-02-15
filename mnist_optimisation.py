# -*- coding: utf-8 -*-
"""MNIST_Optimisation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BeqN-2qdisezjBlp14TJGB_pbrOvUICC
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
import time

# Load and prepare MNIST dataset
print("Loading MNIST dataset...")
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
X = X.astype('float32')
y = y.astype('int32')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_train_encoded = keras.utils.to_categorical(y_train)
y_test_encoded = keras.utils.to_categorical(y_test)

print("Data prepared successfully.")

def create_model(neurons=128, activation='relu', kernel_initializer='he_normal',
                 regularizer=None, dropout_rate=0):
    model = keras.Sequential([
        keras.layers.Input(shape=(784,)),
        keras.layers.Dense(neurons, activation=activation, kernel_initializer=kernel_initializer,
                           kernel_regularizer=regularizer),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model

def train_and_evaluate(model, optimizer, loss, X_train, y_train_encoded, X_test, y_test_encoded,
                       epochs=100, batch_size=32):
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    start_time = time.time()
    history = model.fit(X_train, y_train_encoded, epochs=epochs, batch_size=batch_size,
                        validation_split=0.2, verbose=0)
    end_time = time.time()
    training_time = end_time - start_time

    test_loss, test_accuracy = model.evaluate(X_test, y_test_encoded, verbose=0)

    return history, test_accuracy, training_time

def run_experiment(name, **kwargs):
    print(f"\nRunning experiment: {name}")

    # Extract the optimizer separately
    optimizer = kwargs.pop('optimizer')  # Remove optimizer from kwargs
    loss = kwargs.pop('loss')  # Remove loss from kwargs

    model = create_model(**kwargs)

    history, test_accuracy, training_time = train_and_evaluate(
        model, optimizer, loss, X_train, y_train_encoded, X_test, y_test_encoded
    )

    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Training Time: {training_time:.2f} seconds")

    return history, test_accuracy, training_time


# Baseline model
baseline = run_experiment("Baseline", neurons=128, activation='relu', optimizer='sgd',
                          loss='categorical_crossentropy')

# Experiment 1: Increasing neurons
exp1 = run_experiment("Increased Neurons", neurons=256, activation='relu', optimizer='sgd',
                      loss='categorical_crossentropy')

# Experiment 3: Activation functions
exp3 = run_experiment("Leaky ReLU Activation", neurons=128,
                      activation=keras.layers.LeakyReLU(alpha=0.01), optimizer='sgd',
                      loss='categorical_crossentropy')

# Experiment 5: Regularization
exp5 = run_experiment("L2 Regularization", neurons=128, activation='relu', optimizer='sgd',
                      loss='categorical_crossentropy',
                      regularizer=keras.regularizers.l2(0.01), dropout_rate=0.3)

# Experiment 6: Optimization algorithm
exp6 = run_experiment("Adam Optimizer", neurons=128, activation='relu',
                      optimizer=keras.optimizers.Adam(learning_rate=0.001),
                      loss='categorical_crossentropy')

# Plotting results
experiments = [
    ("Baseline", baseline),
    ("Increased Neurons", exp1),
    ("Leaky ReLU Activation", exp3),
    ("L2 Regularization + Dropout", exp5),
    ("Adam Optimizer", exp6)
]

plt.figure(figsize=(12, 6))
for name, (history, _, _) in experiments:
    plt.plot(history.history['val_accuracy'], label=name)

plt.title('Validation Accuracy Comparison')
plt.xlabel('Epoch')
plt.ylabel('Validation Accuracy')
plt.legend()
plt.show()

# Print summary of results
print("\nSummary of Results:")
print("-------------------")
for name, (_, test_accuracy, training_time) in experiments:
    print(f"{name}:")
    print(f"  Test Accuracy: {test_accuracy:.4f}")
    print(f"  Training Time: {training_time:.2f} seconds")

print("\nExperiments completed. Please refer to the plot and summary for results.")