import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./dane13.txt', header=None, sep='\s', engine='python')

X = data.iloc[:, [0]].values
y = data.iloc[:, [1]].values


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# y = ax + b
cost = np.hstack([X_train, np.ones(X_train.shape)])
v = np.linalg.pinv(cost) @ y_train

print('model 1: y=ax+b')
print(f'params:\n{v}')

plt.plot(X_test, y_test, 'ro')
plt.plot(X_test, v[0]*X_test + v[1], 'b*')
plt.show()

cost = np.hstack([
    X_train ** 4,
    X_train ** 3,
    X_train ** 2,
    X_train,
    np.ones(X_train.shape)
])
v = np.linalg.pinv(cost) @ y_train

print('model 2: y=ax2 + bx + c')
print(f'params:\n{v}')
# print(np.concatenate((X_train, X_test)))
plt.plot(X_test, y_test, 'ro')
plt.plot(X_test, 
        v[0] * (X_test ** 4) +
        v[1] * (X_test ** 3) +
        v[2] * (X_test ** 2) +
        v[3] * X_test + 
        v[4], 'b*')
plt.show()