from db.DataAccessObject import DataAccessObject
from sklearn.linear_model import LogisticRegression
from time import time
import random
import numpy as np
import pickle
random.seed(0)

VERBOSE = True
SIZE = 20000
PATH = r"E:/data"

def print_(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)
    else:
        pass


# Initialize connection to database.
db = DataAccessObject(database="local", collection="grayscale")
training_cursor, testing_cursor, training_size, testing_size = db.partition_dataset(0.8, 0.2, SIZE, gender=1)
print_("----- Dataset obtained -----\n" + \
      f"Training set has {training_size} documents\n" +\
      f"Testing set has {testing_size} documents\n")

# Prepare variables.
print_("----- Loading X, y -----\n")
training_X = []
training_y = []
testing_X = []
testing_y = []

for doc in training_cursor:
    training_X.append(doc["pixels"])
    training_y.append(doc["gender"])
for doc in testing_cursor:
    testing_X.append(doc["pixels"])
    testing_y.append(doc["gender"])

training_X = np.array(training_X)
training_y = np.array(training_y)
testing_X = np.array(testing_X)
testing_y = np.array(testing_y)

print_(f"Dim(training_X) = {training_X.size}, Dim(training_y) = {training_y.size}\n")
print_(f"Dim(testing_X) = {testing_X.size}, Dim(testing_y) = {testing_y.size}\n")

# Train the neural network
nn = LogisticRegression(max_iter=20000, solver="lbfgs")
start_time = time()
print_(f"----- Start training at {start_time} -----\n")
nn.fit(training_X, training_y)
end_time = time()
print_(f"----- Training finished at {end_time} -----\n")
print_(f"Total time involved: {end_time - start_time}\n")

training_y_hat = nn.predict(training_X)
testing_y_hat = nn.predict(testing_X)

print_("Training y: " + str(training_y), end="\n")
print_("Training y_hat: " + str(training_y_hat), end="\n")
print_("Testing y: " + str(testing_y), end="\n")
print_("Testing y_hat: " + str(testing_y_hat), end="\n")

print_("----- Statistics -----")
print_(f"Testing score: {nn.score(testing_X, testing_y)}")

with open("nn.dat", "wb") as fd:
    pickle.dump(nn, fd)

print_("----- Serialization -----")
print_(f"Trained neural network is Pickled in {PATH}/nn.dat")
