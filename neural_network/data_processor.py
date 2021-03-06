from scipy import io as sio
import os
import random

ofp1 = "/Users/data/data_hand_write_numbers_training.mat"
ofp2 = "/Users/data/data_hand_write_numbers_testing.mat"
data = sio.loadmat("/Users/data/data_hand_write_numbers.mat")

X = data['X']
y = data['y']

m = X.shape[0]

for i in range(0, m):
    index = random.randint(i, m-1)
    tmp = X[index, :]
    X[index, :] = X[i, :]
    X[i, :] = tmp
    tmp = y[index, 0]
    y[index, 0] = y[i, 0]
    y[i, 0] = tmp
    y[i, 0] = y[i, 0] % 10

# X = X[0:5, :]
# y = y[0:5, :]

m = int(X.shape[0] * 0.3)

X_test = X[m:, :]
y_test = y[m:, :]
X = X[:m, :]
y = y[:m, :]

dic1 = {}
dic1['X'] = X
dic1['y'] = y

dic2 = {}
dic2['X'] = X_test
dic2['y'] = y_test

if not os.path.isdir(os.path.dirname(ofp1)):
    os.makedirs(os.path.dirname(ofp1))
if os.path.exists(ofp1):
    os.remove(ofp1)
if not os.path.isdir(os.path.dirname(ofp2)):
    os.makedirs(os.path.dirname(ofp2))
if os.path.exists(ofp2):
    os.remove(ofp2)

sio.savemat(file_name=ofp1, mdict=dic1, do_compression=True)
sio.savemat(file_name=ofp2, mdict=dic2, do_compression=True)

print('finish!')