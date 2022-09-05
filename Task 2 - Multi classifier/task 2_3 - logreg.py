import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from plot import plot_decision_regions
from collections import Counter


class LogisticRegressionGD(object):
    def __init__(self, eta=0.05, n_iter=100, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])

        for i in range(self.n_iter):
            net_input = self.net_input(X)
            output = self.activation(net_input)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()

        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, z):
        return 1. / (1. + np.exp(-np.clip(z, -250, 250)))

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)


class Multi_classifier_logreg(object):
    def __init__(self, eta=0.05, n_iter=100, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):
        self.targets = list(Counter(y).keys())
        (self.targets).sort()
        self.logregs = [LogisticRegressionGD(self.eta, self.n_iter, self.random_state)
                        for i in range(len(self.targets))]
        for i in range(len(self.targets)):
            X_subset = X.copy()
            y_subset = y.copy()
            print(list(self.targets)[i])
            y_subset[(y != self.targets[i])] = 0
            y_subset[(y == self.targets[i])] = 1
            self.logregs[i].fit(X_subset, y_subset)

    def predict(self, X):
        res = self.predict_recursive(X, self.logregs, 0)
        return res

    def predict_recursive(self, X, arr, i):
        if i == len(self.targets) - 3:
            return np.where(arr[0].predict(X) == 1, i, np.where(arr[-1].predict(X) == 1, i+2, i+1))
        else:
            return np.where(arr[0].predict(X) == 1, i, self.predict_recursive(X, arr[1:], i+1))

    def predict_for_three(self, X):
        """the same as 'predict' method but solely for three classes"""
        return np.where(self.logregs[0].predict(X) == 1, 0, np.where(self.logregs[-1].predict(X) == 1, 2, 1))

    def predict_sample_belonging(self, sample, target):
        """returns a list of probabilities for each 'sample' element that
        it belongs to 'target' class"""
        perceptron = self.logregs[target]
        return [round(x, 3) for x in perceptron.activation(perceptron.net_input(sample))]


def main():
    iris = datasets.load_iris()
    X = iris["data"][:, [2, 3]]
    y = iris["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1, stratify=y)

    lrgd = Multi_classifier_logreg(eta=0.05, n_iter=1000)
    lrgd.fit(X_train, y_train)

    target = 2
    print("Probability that sample belongs to "+str(target))
    print([(x, y)
          for x, y in zip(lrgd.predict_sample_belonging(X_test, target), y_test)])

    plot_decision_regions(X=X_test,
                          y=y_test, classifier=lrgd)
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
