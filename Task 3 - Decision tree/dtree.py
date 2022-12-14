import numpy as np
import matplotlib.pylab as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from matplotlib.colors import ListedColormap

def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    # generator
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # creating the space
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # creating the graph for all cases
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8, c=cmap(idx), marker=markers[idx], label=cl,
                    edgecolor='black')

    # testing cases
    if test_idx:
        X_test, y_test = X[list(test_idx), :], y[list(test_idx)]
        plt.scatter(X_test[:, 0], X_test[:, 1], edgecolor='black', alpha=1.0, linewidth=1, marker='o',
                    edgecolors='k', s=100, label='test cases')


def main():

    # part 1

    iris = datasets.load_iris()
    X = iris.data[:, [2, 3]]
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

    # standartazing
    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)
    X_combined_std = np.vstack((X_train_std, X_test_std))
    y_combined = np.hstack((y_train, y_test))

    # ---

    # part 2
    tree = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=1)
    tree.fit(X_train, y_train)
    X_combined = np.vstack((X_train, X_test))
    y_combined = np.hstack((y_train, y_test))
    plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105, 150))
    plt.title('DecisionTreeClassifier GINI DEPTH=4')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.legend(loc='upper left')
    plt.savefig('tree-gini-4')
    plt.show()

    tree = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=1)
    tree.fit(X_train, y_train)
    X_combined = np.vstack((X_train, X_test))
    y_combined = np.hstack((y_train, y_test))
    plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105, 150))
    plt.title('DecisionTreeClassifier ENTROPY DEPTH=4')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.legend(loc='upper left')
    plt.savefig('tree-entropy-4')
    plt.show()

    # ---

    # part 3

    tree = DecisionTreeClassifier(criterion='gini', max_depth=10, random_state=1)
    tree.fit(X_train, y_train)
    X_combined = np.vstack((X_train, X_test))
    y_combined = np.hstack((y_train, y_test))
    plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105, 150))
    plt.title('DecisionTreeClassifier GINI DEPTH=10')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.legend(loc='upper left')
    plt.savefig('tree-gini-30')
    plt.show()

    tree = DecisionTreeClassifier(criterion='gini', max_depth=2, random_state=1)
    tree.fit(X_train, y_train)
    X_combined = np.vstack((X_train, X_test))
    y_combined = np.hstack((y_train, y_test))
    plot_decision_regions(X_combined, y_combined, classifier=tree, test_idx=range(105, 150))
    plt.title('DecisionTreeClassifier GINI DEPTH=2')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.legend(loc='upper left')
    plt.savefig('tree-gini-1')
    plt.show()

    # ---

    # part 4

    forest = RandomForestClassifier(criterion='gini', n_estimators=30, random_state=1, n_jobs=2)
    forest.fit(X_train, y_train)
    plot_decision_regions(X_combined, y_combined,
                          classifier=forest, test_idx=range(105, 150))
    plt.title('RandomForestClassifier GINI ESTIMATORS=30')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.legend(loc='upper left')
    plt.savefig('ran-tree-gini-30')
    plt.show()


    forest = RandomForestClassifier(criterion='gini', n_estimators=4, random_state=1, n_jobs=2)
    forest.fit(X_train, y_train)
    plot_decision_regions(X_combined, y_combined,
                          classifier=forest, test_idx=range(105, 150))
    plt.title('RandomForestClassifier GINI ESTIMATORS=4')
    plt.xlabel('length')
    plt.ylabel('width')
    plt.savefig('ran-tree-gini-4')
    plt.show()


if __name__ == '__main__':
    main()
