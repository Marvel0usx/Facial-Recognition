from db.DataAccessObject import DataAccessObject
from sklearn.linear_model import LogisticRegression
import time
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
print_(f"----- Retrieving Data from MongoDB -----\n" + \
      f"Training set has {training_size} documents\n" +\
      f"Testing set has {testing_size} documents\n")

# Prepare variables.
print_("----- Loading X, y -----")
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

print_(f"Dim(training_X) = {training_X.size}, Dim(training_y) = {training_y.size}")
print_(f"Dim(testing_X) = {testing_X.size}, Dim(testing_y) = {testing_y.size}\n")

# Train the neural network
nn = LogisticRegression(max_iter=20000, solver="lbfgs")
start_time = time.time()
print_(f"----- Start training at {time.ctime()} -----")
nn.fit(training_X, training_y)
end_time = time.time()
print_(f"----- Training finished at {time.ctime()} -----\n")
print_("Total time involved: {:.2f}s\n".format(end_time - start_time))

training_y_hat = nn.predict(training_X)
testing_y_hat = nn.predict(testing_X)

print_("----- Testing -----")
print_("Training y: \n" + str(training_y))
print_("Training y_hat: \n" + str(training_y_hat))
print_("Testing y: \n" + str(testing_y))
print_("Testing y_hat: \n" + str(testing_y_hat))

print_("\n----- Statistics -----")
print_(f"Testing score: {nn.score(testing_X, testing_y)}\n")


def store():
    with open("nn.dat", "wb") as fd:
        try:
            pickle.dump(nn, fd)
        except pickle.PicklingError as e:
            print("Error! unable to pickle data!")
            print("Enter <R> to retry.\t")
            if input() == 'r':
                store()
            else:
                exit(1)


print_("----- Serialization -----")
store()
print_(f"Trained neural network is Pickled in {PATH}/nn.dat")
