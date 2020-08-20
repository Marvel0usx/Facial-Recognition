import numpy as np
import seaborn as sns
from db.DataAccessObject import DataAccessObject
from sklearn.linear_model import LogisticRegression
import pickle

PATH = "./"

nn_gender = pickle.load(open(PATH + "nn_gender.dat", "rb"))
nn_age = pickle.load(open(PATH + "nn_age.dat", "rb"))
nn_ethnicity = pickle.load(open(PATH + "nn_ethnicity.dat", "rb"))

dataset = DataAccessObject(database="local", collection="grayscale")
cursor = dataset.get_X_y_pair(20000, 0, **{"gender": True, "age": True, "ethnicity": True})

X = []
y_gender = []
y_age = []
y_ethnicity = []

for raw_data in cursor:
    X.append(raw_data["pixels"])
    y_gender.append(raw_data["gender"])
    y_age.append(raw_data["age"])
    y_ethnicity.append(raw_data["ethnicity"])

X = np.array(X)

y_hat_gender_label = nn_gender.predict(X)

y_hat_gender = nn_gender.predict(X)
y_hat_age = nn_age.predict(X)
y_hat_ethnicity = nn_ethnicity.predict(X)


# Confusion matrix and heatmap.
def confusion_matrix(y_hat, y_truth, criterion):
    """Function that returns the confusion matrix of the given data set."""
    tp = tn = fp = fn = 0
    # Calculate for True Positive
    for idx in range(len(y_hat)):
        if y_truth[idx] == criterion:
            if y_hat[idx] == y_truth[idx]:
                tp += 1
            else:
                fp += 1
        else:
            if y_hat[idx] == y_truth[idx]:
                tn += 1
            else:
                fn += 1

    print(f"----- Confusion Matrix -----")
    print(f"True Negative: {tn} False Positive: {fp}")
    print(f"False Negative: {fn} True Positive: {tp}")
    return tp, fp, tn, fn


def plot_confusion_matrix(true_negative, false_positive, false_negative, true_positive, axis_labels=[]):
    total = true_positive + false_positive
    data = np.array([[true_negative, false_positive], [false_negative, true_positive]])
    labels = np.asarray([f"True Neg\n{true_negative}\n{true_negative / total:.2%}",
                         f"False Pos\n{false_positive}\n{false_positive / total:.2%}",
                         f"False Neg\n{false_negative}\n{false_negative / total:.2%}",
                         f"True Pos\n{true_positive}\n{true_positive / total:.2%}"]
                        ).reshape((2, 2))
    fig = sns.heatmap(data, annot=labels, xticklabels=axis_labels, yticklabels=axis_labels,
                      fmt="", cmap="Blues").get_figure()
    fig.savefig("confusion_matrix.png")


true_positive, false_positive, true_negative, false_negative = confusion_matrix(y_hat_gender, y_gender, "female")

plot_confusion_matrix(true_negative, false_positive, false_negative, true_positive, ["male", "female"])


# Calculate for McFadden's pseudo R-squared
def logit(x, w):
    return 1 / (1 + np.exp(-np.dot(x, w.T)))


def lc_log_likelihood(w, X, y):
    """Function that calculates for the log-likelihood of a linear regression model."""
    log_likelihood = 0
    for idx in range(len(y)):
        log_likelihood += y[idx] * np.log(logit(X[idx], w)) + (1 - y[idx]) * np.log(1 - logit(X[idx], w))
    return log_likelihood


def mcfadden_rsquared(trained_weight, null_weight, X, y):
    trained_log_likelihood = lc_log_likelihood(trained_weight, X, y)
    null_log_likelihood = lc_log_likelihood(null_weight, X, y)
    return 1.0 - (trained_log_likelihood / null_log_likelihood)


y_for_log_likelihood = [0 if g == "male" else 1 for g in y_gender]
# print(mcfadden_rsquared(nn_gender.coef_, np.array([w if i == 0 else 0.0 for i, w in enumerate(nn_gender.coef_)]),
#                         X, y_for_log_likelihood))

def full_log_likelihood(w, X, y):
    score = np.dot(X, w).reshape(1, X.shape[0])
    return np.sum(-np.log(1 + np.exp(score))) + np.sum(y * score)

def null_log_likelihood(w, X, y):
    z = np.array([w if i == 0 else 0.0 for i, w in enumerate(w.reshape(1, X.shape[1])[0])]).reshape(X.shape[1], 1)
    score = np.dot(X, z).reshape(1, X.shape[0])
    return np.sum(-np.log(1 + np.exp(score))) + np.sum(y * score)

def mcfadden_rsquare(w, X, y):
    return 1.0 - (full_log_likelihood(w, X, y) / null_log_likelihood(w, X, y))

print(mcfadden_rsquare(nn_gender.coef_.T, X, np.array(y_for_log_likelihood)))