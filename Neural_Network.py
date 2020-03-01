from os import listdir
import pickle
import numpy as np


def sigm(x, deriv=False):
    if deriv:
        return sigm(x) * (1 - sigm(x))
    return 1 / (1 + np.exp(-x))


train_data = []
train_out = []
file_count = 0


if __name__ == '__main__':
    for file_name in listdir('./Boolean_train'):
        file_count += 1
        f = open(f'./Boolean_train/{file_name}', 'rb')
        data = pickle.load(f)
        f.close()
        file_name = file_name.split('_')
        train_data.append(data)
        train_out.append(file_name[0])

    for elem in range(len(train_out)):
        if train_out[elem] == 'True':
            train_out[elem] = 1
        else:
            train_out[elem] = 0

    print(train_data)
    print(train_out)

    train_data = np.array([train_data])
    train_out = np.array([train_out]).T

    synaptic_weight = 2 * np.random.random((625, 1)) - 1
    train_data.shape = (file_count, 625)

    for i in range(2000):
        outputs = sigm(np.dot(train_data, synaptic_weight))

        err = train_out - outputs

        adjustments = np.dot(train_data.T, err * (outputs * (1 - outputs)))

        synaptic_weight += adjustments

    f = open('weights.goose', 'wb')
    pickle.dump(synaptic_weight, f)
    f.close()
    print(outputs)
