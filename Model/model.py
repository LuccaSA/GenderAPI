import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Define hyper parameters
epochs = 100
batch_size = 2000
epsilon = 0.006
fc1_size = 256

# Read dataset
X_TRAIN = np.load("./npy/X_TRAIN.npy")
Y_TRAIN = np.load("./npy/Y_TRAIN.npy")
X_TEST = np.load("./npy/X_TEST.npy")
Y_TEST = np.load("./npy/Y_TEST.npy")
X_VAL = np.load("./npy/X_VAL.npy")
Y_VAL = np.load("./npy/Y_VAL.npy")

# Define placholders
inputs = tf.placeholder(shape=(None, 40), name="inputs", dtype=tf.float32)
labels = tf.placeholder(shape=(None, ), name="labels", dtype=tf.int64)

# Layer fully connected
fc1_w = tf.get_variable(name="weights_fc1", shape=(40, fc1_size), dtype=tf.float32)
fc1_b = tf.get_variable(name="bias_fc1", shape=(fc1_size), dtype=tf.float32)
fc1 = tf.nn.relu(tf.matmul(tf.reshape(inputs, shape=(-1, 40)), fc1_w) + fc1_b)

# output layer : 128 => 2
output_w = tf.get_variable(name="weights", shape=(fc1_size, 2))
output_b = tf.get_variable(name="bias", shape=(2))

# logit & predictions
logits = tf.matmul(fc1, output_w) + output_b
predictions = tf.argmax(tf.nn.softmax(logits), axis=1)

# labels
one_hot_labels = tf.one_hot(labels, 2)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=one_hot_labels, logits=logits))

# optimizer
optimizer = tf.train.AdamOptimizer(epsilon).minimize(loss)

# accuray
accuracy = tf.reduce_mean(tf.cast(tf.equal(labels, predictions), dtype=tf.float32))

saver = tf.train.Saver(max_to_keep=1)

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
            _, lo, ac = sess.run([optimizer, loss, accuracy],
                                 feed_dict={
                                     inputs: X_TRAIN[train_step * batch_size:(train_step + 1) * batch_size],
                                     labels: Y_TRAIN[train_step * batch_size:(train_step + 1) * batch_size]
                                           })
                                           
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
    
    saver.save(sess, "./model_fc256.ckpt")
    
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
