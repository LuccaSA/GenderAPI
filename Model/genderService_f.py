import os
import sys
import tensorflow as tf
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Define hyper parameters
fc1_size = 256

# Define placholders
inputs = tf.placeholder(shape=(None, 40), name="inputs", dtype=tf.float32)

# Layer fully connected
fc1_w = tf.get_variable(name="weights_fc1", shape=(40, fc1_size), dtype=tf.float32)
fc1_b = tf.get_variable(name="bias_fc1", shape=(fc1_size), dtype=tf.float32)
fc1 = tf.nn.relu(tf.matmul(tf.reshape(inputs, shape=(-1, 40)), fc1_w) + fc1_b)

# output layer : 128 => 2
output_w = tf.get_variable(name="weights", shape=(fc1_size, 2))
output_b = tf.get_variable(name="bias", shape=(2))

# logit & predictions
logits = tf.matmul(fc1, output_w) + output_b
predictions = tf.nn.softmax(logits)

saver = tf.train.Saver(max_to_keep=1)

def encode(input):
    maxFnameLen = 40 # nb de caractères max dans le prénom
    # si prénom trop long on fait planter
    if (len(input) > maxFnameLen):
        print("Too big name detected : " + input)
        return;
    fnameAdj = '{0: <{l}}'.format(input[::], l=maxFnameLen)[0:maxFnameLen].upper()
    result = []
    for c in fnameAdj:
        v = 1 + ord(c) - ord('A')
        if v < 0:
            v = 0
        result.append(v)
    return result

if len(sys.argv) != 2:
    print("Vous devez envoyer un prenom comme argument de la commande")
    sys.exit()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    current_path = os.path.dirname(os.path.realpath(__file__))
    saver.restore(sess, current_path + "/model_fc256.ckpt")
        
    X_ASK = [ encode(sys.argv[1]) ]
    
    pred = sess.run([predictions],
                                 feed_dict={
                                     inputs: X_ASK
                                           })

                                           
           

    boyperc = pred[0][0][0]
    
    print()

    if (boyperc > 0.5):
        print("C'est un garçon à %d %%" % int(100 * pred[0][0][0]))

    if (boyperc < 0.5):
        print("C'est une fille à %d %%" % int(100 * pred[0][0][1]))
