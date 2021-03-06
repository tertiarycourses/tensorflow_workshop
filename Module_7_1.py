# Tensorflow workshop with Jan Idziak
#-------------------------------------
#
#script harvested from:
#https://pythonprogramming.net
#
# Implementing Convolutional Neural Network
#---------------------------------------
#
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("data/", one_hot = True)

n_classes = 10
batch_size = 128


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def maxpool2d(x):
    #size of window movement of window
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

graph = tf.Graph()

with graph.as_default():
    weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,1,32])),
               'W_conv2':tf.Variable(tf.random_normal([5,5,32,64])),
               'W_fc':tf.Variable(tf.random_normal([7*7*64,1024])),
               'out':tf.Variable(tf.random_normal([1024, n_classes]))}

    biases = {'b_conv1':tf.Variable(tf.random_normal([32])),
               'b_conv2':tf.Variable(tf.random_normal([64])),
               'b_fc':tf.Variable(tf.random_normal([1024])),
               'out':tf.Variable(tf.random_normal([n_classes]))}

    x = tf.placeholder('float', [None, 784])
    y = tf.placeholder('float')
    keep_prob = tf.placeholder(tf.float32)

    inp = tf.reshape(x, shape=[-1, 28, 28, 1])

    conv1 = tf.nn.relu6(conv2d(inp, weights['W_conv1']) + biases['b_conv1'])
    conv1 = maxpool2d(conv1)
    
    conv2 = tf.nn.softsign(conv2d(conv1, weights['W_conv2']) + biases['b_conv2'])
    conv2 = maxpool2d(conv2)

    fc = tf.reshape(conv2,[-1, 7*7*64])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc'])+biases['b_fc'])
    fc = tf.nn.dropout(fc, keep_prob)

    output = tf.matmul(fc, weights['out'])+biases['out']
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    correct = tf.equal(tf.argmax(output, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

def train_neural_network(x):

    hm_epochs = 3
    with tf.Session(graph=graph) as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y, keep_prob: 0.8})
                epoch_loss += c

            print('Epoch', epoch+1, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        acc = []
        for i in range(100):
            acc.append(accuracy.eval({x: mnist.test.images[(1 + (i*100)):((i+1)*100),], y: mnist.test.labels[(1 + (i*100)):((i+1)*100),], keep_prob:1}))
        print('Accuracy:', sess.run(tf.reduce_mean(acc)))

train_neural_network(x)

#Prepare CNN neural network for the Iris data.
#Use:
# - Two conwolutional layers 
# (filter size: first: 5, returns: 16, second: 3, returns:32) 
# - Two pooling layers
# - reshape to appropriate size for the fully connected layer

# Train the network for 3 epochs 
# Use bach size of 100
# Calculate accuracy for just 5000 first observations from train set
