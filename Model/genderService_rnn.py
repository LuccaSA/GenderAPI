import os
import sys
import tensorflow as tf
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Define hyper parameters
fc1_size = 128
FC_decoder = 128
RNN_SIZE = 128
seq_len = 40 

# Define placholders
inputs = tf.placeholder(shape=(None, 40, 27), name="inputs", dtype=tf.float32)

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

predictions = []

for t in range(seq_len):
    with tf.variable_scope('lstm', reuse=(t != 0)):
         _, (c, h) = cell(inputs=tf.zeros((1,1)), state=(c, h))

    logits = tf.matmul(h, FC_output_w) + FC_output_b
    predictions.append(tf.argmax(logits, -1, output_type=tf.int64))

saver = tf.train.Saver(max_to_keep=1)

def encode(input):
    maxFnameLen = 40 # nb de caractères max dans le prénom
    lettersToReplace = "ÀÁÂÃÄÅàáâãäåÒÓÔÕÖØòóôõöøÈÉÊËèéêëÌÍÎÏìíîïÙÚÛÜùúûüÿÑñÇç";
    replacementletters = "AAAAAAaaaaaaOOOOOOooooooEEEEeeeeIIIIiiiiUUUUuuuuyNnCc";

    # si prénom trop long on fait planter
    if (len(input) > maxFnameLen):
        print("Too big name detected : " + input)
        return;
        
    #Accent insensitive
    for i in range(0, len(lettersToReplace)):
        input = input.replace(lettersToReplace[i], replacementletters[i])
        
    fnameAdj = '{0: <{l}}'.format(input[::], l=maxFnameLen)[0:maxFnameLen].upper()
    result = []
    for c in fnameAdj:
        v = 1 + ord(c) - ord('A')
        if v < 0 or v > 26:
            v = 0
        one_hot = np.zeros(27)
        one_hot[v] = 1
        result.append(one_hot.tolist())
    return result

if len(sys.argv) != 2:
    print("Vous devez envoyer un prenom comme argument de la commande")
    sys.exit()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    current_path = os.path.dirname(os.path.realpath(__file__))
    saver.restore(sess, current_path + "/model_rnn_ci_ai_matrices.ckpt")
        
    X_ASK = [ encode(sys.argv[1]) ]
    
    pred = sess.run([predictions],
                                 feed_dict={
                                     inputs: X_ASK
                                           })

                                           
           

    print(pred[0][0], pred[0][1], pred[0][2], pred[0][3], pred[0][4], pred[0][5], pred[0][6], pred[0][7], pred[0][8], pred[0][9], pred[0][10], pred[0][11])