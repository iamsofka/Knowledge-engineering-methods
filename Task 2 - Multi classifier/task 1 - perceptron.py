import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from plot import plot_decision_regions
from collections import Counter


class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)


class Multi_classifier_perceptron(object):
    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        self.targets = list(Counter(y).keys())  # [0,1,2]
        (self.targets).sort()
        self.perceptrons = [Perceptron(self.eta, self.n_iter)
                            for i in range(len(self.targets))]
        for i in range(len(self.targets)):
            X_subset = X.copy()
            y_subset = y.copy()
            print(list(self.targets)[i])
            y_subset[(y != self.targets[i])] = -1
            y_subset[(y == self.targets[i])] = 1
            self.perceptrons[i].fit(X_subset, y_subset)

    def predict(self, X):
        res = self.predict_recursive(X, self.perceptrons, 0)
        return res

    def predict_recursive(self, X, arr, i):
        if i == len(self.targets) - 3:
            return np.where(arr[0].predict(X) == 1, i, np.where(arr[-1].predict(X) == 1, i+2, i+1))
        else:
            return np.where(arr[0].predict(X) == 1, i, self.predict_recursive(X, arr[1:], i+1))

    def predict_for_three(self, X):
        """the same as 'predict' method but solely for three classes"""
        return np.where(self.perceptrons[0].predict(X) == 1, 0, np.where(self.perceptrons[-1].predict(X) == 1, 2, 1))


def main():

    iris = datasets.load_iris()
    X = iris["data"][:, [2, 3]]
    y = iris["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1, stratify=y)

    multi_perceptron = Multi_classifier_perceptron(eta=0.2, n_iter=200)
    multi_perceptron.fit(X_train, y_train)

    plot_decision_regions(X=X_test,
                          y=y_test, classifier=multi_perceptron)
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
