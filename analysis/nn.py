from db.DataAccessObject import DataAccessObject
from sklearn.linear_model import LogisticRegression
from time import time
import random
import numpy as np
from PIL import Image
import pickle
random.seed(0)

VERBOSE = False


def print_(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)
    else:
        pass


# Initialize connection to database.
db = DataAccessObject(database="local", collection="grayscale")
training_dataset, testing_dataset = db.partition_dataset(training=0.8, testing=0.2)
print_("----- Dataset obtained -----\n" + \
      f"Training set has {training_dataset.count_documents({})} documents\n" +\
      f"Testing set has {testing_dataset.count_documents({})} documents\n")

# Prepare variables.
print_("----- Loading X, y -----\n")
training_X = np.array([p for p in training_dataset["pixels"]])
training_y = np.array(training_dataset["gender"])
testing_X = np.array([p for p in testing_dataset["pixels"]])
testing_y = np.array(testing_dataset["gender"])
print_(f"Dim(X) = {training_X.size}, Dim(y) = {training_y.size}\n")
print_(f"Training set composes of {training_dataset.count_documents({'gender': 'male'})} males, and" +
       f"{training_dataset.count_documents({'gender': 'female'})} females.")

# Train the neural network
nn = LogisticRegression(max_iter=20000, solver="lbfgs")
start_time = time()
print_(f"----- Start training at {start_time} -----\n")
nn.fit(training_X, training_y)
end_time = time()
print_(f"----- Training finished at {end_time} -----\n")
print_(f"Total time involved: {end_time - start_time}\n")

y_hat_train = nn.predict(training_X)
y_hat_test = nn.predict(testing_X)