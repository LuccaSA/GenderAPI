import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Define hyper parameters
epochs = 10
batch_size = 2000
epsilon = 0.003
fc1_size = 128
FC_decoder = 128
seq_len = 40 # doit être égal au nombre d'entrées, ici 40 lettres par prénom

RNN_SIZE = 128

# Read dataset
X_TRAIN = np.load("./npy_matrices/X_TRAIN.npy")
Y_TRAIN = np.load("./npy_matrices/Y_TRAIN.npy")
X_TEST = np.load("./npy_matrices/X_TEST.npy")
Y_TEST = np.load("./npy_matrices/Y_TEST.npy")
X_VAL = np.load("./npy_matrices/X_VAL.npy")
Y_VAL = np.load("./npy_matrices/Y_VAL.npy")
n_train = len(X_TRAIN)

# Define placholders
inputs = tf.placeholder(shape=(None, 40, 27), name="inputs", dtype=tf.float32)
labels = tf.placeholder(shape=(None, ), name="labels", dtype=tf.int64)

# Layer fully connected
fc1_w = tf.get_variable(name="weights_fc1", shape=(40 * 27, fc1_size), dtype=tf.float32)
fc1_b = tf.get_variable(name="bias_fc1", shape=(fc1_size), dtype=tf.float32)
fc1 = tf.nn.relu(tf.matmul(tf.reshape(inputs, shape=(-1, 40 * 27)), fc1_w) + fc1_b)

features_proj = tf.reshape(fc1, [-1, 1, fc1_size]) # on repasse en 3D (on récupère donc la dimension des time steps)

# init 
cell_fw_1 = tf.contrib.rnn.GRUCell(RNN_SIZE)
cell_bw_1 = tf.contrib.rnn.GRUCell(RNN_SIZE)

H, _ = tf.nn.bidirectional_dynamic_rnn(cell_fw_1, cell_bw_1, features_proj, dtype=tf.float32)

H = tf.concat([H[0], H[1]], axis=2) # on additionne le résultat des 2 directions de RNN

cell = tf.contrib.rnn.BasicLSTMCell(FC_decoder)

mean_features = tf.reduce_mean(H, axis=1)

w_h = tf.get_variable(name="init_h_w", shape=[mean_features.shape[1], FC_decoder])
b_h = tf.get_variable(name="init_h_b", shape=[FC_decoder])
fc_h_0 = tf.nn.tanh(tf.matmul(mean_features,w_h)+b_h)
w_c = tf.get_variable(name="init_c_w", shape=[mean_features.shape[1], FC_decoder])
b_c = tf.get_variable(name="init_c_b", shape=[FC_decoder])
fc_c_0 = tf.nn.tanh(tf.matmul(mean_features,w_c)+b_c)
(c, h) = (fc_c_0, fc_h_0)

# output layer : 128 => 2
FC_output_w = tf.get_variable(name="FC_output_w", shape=(FC_decoder, 2))
FC_output_b = tf.get_variable(name="FC_output_b", shape=(2))

loss = 0.0
predictions = []

for t in range(seq_len):
    with tf.variable_scope('lstm', reuse=(t != 0)):
         _, (c, h) = cell(inputs=tf.zeros((batch_size, 1)), state=(c, h))

    logits = tf.matmul(h, FC_output_w) + FC_output_b
    predictions.append(tf.argmax(logits, -1, output_type=tf.int64))

    loss += tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels))

# tf_predictions = tf.stack(predictions, axis=1)
optimizer = tf.train.AdamOptimizer(epsilon).minimize(loss)
friendly_accuracy = tf.reduce_mean(tf.cast(tf.equal(labels, predictions), dtype=tf.float32))
accuracy = tf.reduce_mean(tf.cast(tf.reduce_all(tf.equal(labels, predictions), 0), dtype=tf.float32))

index_train = np.arange(n_train)

saver = tf.train.Saver(max_to_keep=1)

# labels
# one_hot_labels = tf.one_hot(labels, 2)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

	# Create arrays for loss and accuracy curves plots
    train_accuracies = []
    test_accuracies = []
    train_losses = []
    test_losses = []

    for e in range(epochs):
        print("running epoch %d" % e)
        train_acc = 0
        train_loss = 0
        nb_train_steps = int(len(X_TRAIN) / batch_size)
        for train_step in range(nb_train_steps):
            print("running training batch %d" % train_step)
            _, lo, ac, pred = sess.run([optimizer, loss, accuracy, predictions],
                                 feed_dict={
                                     inputs: X_TRAIN[train_step * batch_size:(train_step + 1) * batch_size],
                                     labels: Y_TRAIN[train_step * batch_size:(train_step + 1) * batch_size]
                                           })
            #print(pred)
            train_acc+=ac
            train_loss+=lo
			
        train_losses.append(train_loss/nb_train_steps)
        train_accuracies.append(train_acc/nb_train_steps)

        print(train_acc/nb_train_steps)

        test_acc = 0
        test_loss = 0
        nb_test_steps = int(len(X_TEST) / batch_size)
        for test_step in range(int(len(X_TEST) / batch_size)):
            print("running test batch %d" % test_step)
            l, acc = sess.run([loss, accuracy],
                                 feed_dict={
                                    inputs: X_TEST[test_step * batch_size:(test_step + 1) * batch_size],
                                    labels: Y_TEST[test_step * batch_size:(test_step + 1) * batch_size]
                                 })
            test_acc += acc
            test_loss += l

        test_losses.append(test_loss/nb_test_steps)
        test_accuracies.append(test_acc/nb_test_steps)

        print(test_acc/nb_test_steps)

    #Validation
    val_acc = 0
    val_loss = 0
    nb_val_steps = int(len(X_VAL) / batch_size)
    for val_step in range(int(len(X_VAL) / batch_size)):
        print("running validation batch %d" % val_step)
        l, acc = sess.run([loss, accuracy],
							 feed_dict={
								inputs: X_VAL[val_step * batch_size:(val_step + 1) * batch_size],
								labels: Y_VAL[val_step * batch_size:(val_step + 1) * batch_size]
							 })
        val_acc += acc
        val_loss += l

    print(val_acc/nb_val_steps)
    
    saver.save(sess, "./model_rnn_ci_ai_matrices.ckpt")
    
    # Plot losses
    plt.plot(range(len(test_losses)), test_losses, label="test")
    plt.plot(range(len(train_losses)), train_losses, label="train")
    plt.legend()
    plt.show()

    # Plot accuracies
    plt.plot(range(epochs), test_accuracies, label="test")
    plt.plot(range(epochs), train_accuracies, label="train")
    plt.legend()
    plt.show()
