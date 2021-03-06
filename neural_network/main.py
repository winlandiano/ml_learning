from scipy import io as sio
import numpy as np
from scipy import optimize
import sys

# using a one hidden layer with 25 nodes model, which is recommended by ML Stanford
# the input data has 5000 samples with each 40 features, namely 20x20 pixels

cal_counter = 0
global_cost = 0


def get_weight_matrix(parama, inputs, hiddens, outputs):
    m1 = parama[0:(inputs + 1) * hiddens].reshape(inputs + 1, hiddens)
    m2 = parama[(inputs + 1) * hiddens:].reshape((hiddens + 1), outputs)
    return m1, m2


def load_data(training_file_path, testing_file_path):
    print("start loading data...")
    data = sio.loadmat(training_file_path)
    X_loa = data['X']
    Y_loa = data['y']
    X_loa = np.hstack((np.ones(shape=(X_loa.shape[0], 1), dtype=float), X_loa))  # add bias
    data = sio.loadmat(testing_file_path)
    X_test_loa = data['X']
    Y_test_loa = data['y']
    X_test_loa = np.hstack((np.ones(shape=(X_test_loa.shape[0], 1), dtype=float), X_test_loa))  # add bias
    print("load data finish!")
    return X_loa, Y_loa, X_test_loa, Y_test_loa


def sigmoid(M):
    return 1.0 / (1.0 + np.exp(-M))


def feed_fwd(X_fee, w1_fee, w2_fee):
    m_fee = X_fee.shape[0]
    input_hidden_layer_fee = np.dot(X_fee, w1_fee)
    output_hidden_layer_fee = np.hstack((np.ones(shape=(m_fee, 1), dtype=int), sigmoid(input_hidden_layer_fee)))
    input_output_layer_fee = np.dot(output_hidden_layer_fee, w2_fee)
    output_output_layer_fee = sigmoid(input_output_layer_fee)
    return input_hidden_layer_fee, output_hidden_layer_fee, input_output_layer_fee, output_output_layer_fee


def cost_function(nn_weights_cos, X_cos, Y_logic_cos, my_lambda_cos, hidden_layer_size_cos, input_layer_size_cos,
                  K_cos):
    global cal_counter
    global global_cost
    m = Y_logic_cos.shape[0]
    w1_cos, w2_cos = get_weight_matrix(nn_weights_cos, input_layer_size, hidden_layer_size, K_cos)

    input_hidden_layer_cos, output_hidden_layer_cos, input_output_layer_cos, output_output_layer_cos \
        = feed_fwd(X_cos, w1_cos, w2_cos)

    tmp = Y_logic_cos * np.log(output_output_layer_cos) + (1 - Y_logic_cos) * np.log(1 - output_output_layer_cos)
    J_cos = -1 * np.sum(np.sum(tmp))

    w1_cos[:, 0] = 0
    w2_cos[:, 0] = 0
    J_cos += (np.sum(np.sum(w1_cos ** 2, 0)) + np.sum(np.sum(w2_cos ** 2, 0))) * (my_lambda_cos / 2)
    J_cos = J_cos / m
    global_cost = J_cos
    cal_counter += 1
    sys.stdout.write(
        "\rcost or gradient function called=>" + str(cal_counter) + " with cost function=>" + str(global_cost))
    sys.stdout.flush()
    return J_cos


def gradient(nn_weights_gra, X_gra, Y_logic_gra, my_lambda_gra, hidden_layer_size_gra, input_layer_size_gra, K_gra):
    global cal_counter
    global global_cost

    m = Y_logic_gra.shape[0]
    w1_gra, w2_gra = get_weight_matrix(nn_weights_gra, input_layer_size_gra, hidden_layer_size_gra, K_gra)

    input_hidden_layer_gra, output_hidden_layer_gra, input_output_layer_gra, output_output_layer_gra \
        = feed_fwd(X_gra, w1_gra, w2_gra)

    # backward propagation
    err_out_gra = output_output_layer_gra - Y_logic_gra

    err_hidden_gra = np.dot(err_out_gra, w2_gra.transpose()) * output_hidden_layer_gra * (1 - output_hidden_layer_gra)
    err_hidden_gra = err_hidden_gra[:, 1:]

    delta_input = np.dot(X_gra.transpose(), err_hidden_gra)
    norm = my_lambda_gra * w1_gra
    norm[:, 0] = 0
    delta_input = delta_input + norm
    delta_input = delta_input / m

    delta_hidden = np.dot(output_hidden_layer_gra.transpose(), err_out_gra)
    norm = my_lambda_gra * w2_gra
    norm[:, 0] = 0
    delta_hidden = delta_hidden + norm
    delta_hidden = delta_hidden / m

    cal_counter += 1
    sys.stdout.write(
        "\rcost or gradient function called=>" + str(cal_counter) + " with cost function=>" + str(global_cost))
    sys.stdout.flush()
    return np.hstack((delta_input.reshape(delta_input.size), delta_hidden.reshape(delta_hidden.size)))


# def update_weight(w1, w2, delta1, delta2, learning_rate):
#     '''
#     **discarded**
#     update w1 and w2 according to the result of backward propagation
#     :param w1: weight between input layer and hidden layer
#     :param w2: weight between hidden layer and output layer
#     :param delta1: partial derivative for weight between input and hidden layer
#     :param delta2: partial derivative for weight between hidden layer and output layer
#     :return: ans1:new w1  and  ans2: new w2
#     '''
#     ans1 = w1 + learning_rate * delta1
#     ans2 = w2 + learning_rate * delta2
#     return ans1, ans2


def predict(o_p):
    '''
    :param o_p: value of output layer
    :return: vector of prediction: predic
    '''
    pre = np.argmax(o_p, 1)
    return pre


def make_logic_matrix(Y_mak, K_mak):
    m = Y_mak.shape[0]
    ans = np.ndarray(shape=(m, K_mak), dtype=int)
    tmp = np.linspace(1, K_mak, K_mak, dtype=int)
    for i in range(0, m):
        ans[i, :] = (Y_mak[i, 0] == tmp).astype(int)  # here is really trick!! Mark it!
    return ans


def evaluate_neural_network(X_test_eva, Y_test_eva, w1_eva, w2_eva):
    # TODO
    input_hidden_layer, output_hidden_layer, input_output_layer, output_output_layer = feed_fwd(X_test_eva, w1_eva,
                                                                                                w2_eva)
    Y_pred = predict(output_output_layer)
    m_test = Y_test_eva.shape[0]
    correct_num = np.sum((Y_pred == Y_test_eva).astype(int), 0)[0]
    print("%d correct on %d test sets, accuracy=%f%%" % (correct_num, m_test, (correct_num * 100) / m_test))


if __name__ == '__main__':
    training_file_path = "/Users/data/data_hand_write_numbers_training.mat"
    testing_file_path = "/Users/data/data_hand_write_numbers_testing.mat"
    iteration = 5000
    # learning_rate = 0.1
    hidden_layer_size = 25
    input_layer_size = 400
    K = 10
    my_lambda = 3
    epsilon = 0.12
    '''
    iteration: iterations of feed forward and backward propagation
    # learning_rate: learning rate of gradient decent, which is actually been used here
    hidden_node_num: since we have only on hidden layer, it's convenient to store it
    K: the size of cluster
    my_lambda: panalty rate, applied on the params against over fitting
    epsilon: range for randomly initialize w1 and w2
    '''

    X, Y, X_test, Y_test = load_data(training_file_path, testing_file_path)

    Y_logic = make_logic_matrix(Y, K)
    w1 = np.random.random_sample((input_layer_size + 1) * hidden_layer_size) * 2 * epsilon - epsilon
    w2 = np.random.random_sample((hidden_layer_size + 1) * K) * 2 * epsilon - epsilon

    print("learning training samples...")
    result = optimize.minimize(fun=cost_function, x0=np.hstack((w1, w2)), jac=gradient, method='Newton-CG',
                               args=(X, Y_logic, my_lambda, hidden_layer_size, input_layer_size, K),
                               options={'maxiter': 40})
    if result.success:
        print("\nlearning finish, success")
    else:
        print("\nlearning faild, because", result.message)

    print("evalusating neural network...")
    x_opt = result.x
    w1, w2 = get_weight_matrix(x_opt, input_layer_size, hidden_layer_size, K)

    evaluate_neural_network(X_test, Y_test, w1, w2)
