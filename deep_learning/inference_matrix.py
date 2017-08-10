# read from matrix 

import tensorflow as tf

# construct a convolutional neural network read from a matrix

# randomly construct a 200*10 matrix 
# INPUT_NODE = 10000
# INPUT_NODE = 784
# INPUT_NODE = 122*1513 = 184586(122, 1513, 999)
INPUT_NODE = 184586
# 10*500
# INPUT_NODE = 5000
# INPUT_NODE = 3200
# INPUT_NODE = 1000

OUTPUT_NODE = 2
# OUTPUT_NODE = 3
# OUTPUT_NODE = 4
# OUTPUT_NODE = 5

# MATRIX_LENGTH = 100
# MATRIX_WIDTH = 100

# IMAGE_SIZE = 28
MATRIX_LENGTH = 1513
MATRIX_WIDTH = 122

# MATRIX_LENGTH = 500
# MATRIX_WIDTH = 10
# MATRIX_LENGTH = 400
# MATRIX_WIDTH = 8

# MATRIX_LENGTH = 200
# MATRIX_WIDTH = 5

NUM_CHANNELS = 1

# NUM_LABELS = 3
NUM_LABELS = 2
# NUM_LABELS = 4
# NUM_LABELS = 5

# The size and depth of the first layer of cnn

# CONV1_DEEP = 32
CONV1_DEEP = 8
# CONV1_DEEP = 16
# CONV1_SIZE = 5
# CONV1_SIZE = 3
# CONV1_SIZE = 2
# CONV1_SIZE = 10
CONV1_SIZE = 15

# The size and depth of the first layer of cnn

# CONV2_DEEP = 64
# CONV2_DEEP = 32
CONV2_DEEP = 16
# CONV2_SIZE = 5
CONV2_SIZE = 15
# CONV2_SIZE = 10
# CONV2_SIZE = 3
# CONV2_SIZE = 2

# FC_SIZE = 32, 
FC_SIZE = 128
# FC_SIZE = 128
# FC_SIZE = 16

# define the cnn process

# train 
def inference (input_tensor, train, regularizer):
    # use 0 to pad
    
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable("weight",[CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS, CONV1_DEEP],initializer = tf.truncated_normal_initializer(stddev = 0.1))
        conv1_biases = tf.get_variable("bias", [CONV1_DEEP],initializer = tf.constant_initializer(0.0))
        
        # filter
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides = [1,1,1,1], padding = 'SAME')
        
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1,conv1_biases))
    
    # pooling layer
    
    with tf.name_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(relu1, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')
     
    # second cnn layer
    with tf.variable_scope('layer3-conv2'):
        
        conv2_weights = tf.get_variable("weight",[CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],initializer = tf.truncated_normal_initializer(stddev = 0.1))
        conv2_biases = tf.get_variable("bias", [CONV2_DEEP],initializer = tf.constant_initializer(0.0))
        
        # filter
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides = [1,1,1,1], padding = 'SAME')
        
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2,conv2_biases))
        
    # second pooling layer
    
    with tf.name_scope('layer4-pool2'):
        
        pool2 = tf.nn.max_pool(relu2, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')
        
    pool_shape = pool2.get_shape().as_list()
    
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]
    
    reshaped = tf.reshape(pool2,[pool_shape[0],nodes])
    
    # full connected layer
    
    with tf.variable_scope('layer5-fc1'):
        
        fc1_weights = tf.get_variable("weight",[nodes,FC_SIZE],initializer = tf.truncated_normal_initializer(stddev = 0.1))
        
        # weights of fc layer needs to be initialized
        
        if regularizer != None:
            tf.add_to_collection('losses',regularizer(fc1_weights))
        fc1_biases = tf.get_variable("bias", [FC_SIZE],initializer = tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(reshaped,fc1_weights) + fc1_biases)
        
        if train: fc1 = tf.nn.dropout(fc1,0.5)
    
    with tf.variable_scope('layer6-fc2'):
        
        fc2_weights = tf.get_variable("weight",[FC_SIZE,NUM_LABELS],initializer = tf.truncated_normal_initializer(stddev = 0.1))
        if regularizer != None:
            tf.add_to_collection('losses',regularizer(fc2_weights))
        
        fc2_biases = tf.get_variable("bias", [NUM_LABELS],initializer = tf.constant_initializer(0.1))
        
        logit = tf.matmul(fc1,fc2_weights) + fc2_biases
        
        # logit = tf.nn.relu(tf.matmul(fc1,fc2_weights) + fc2_biases)
        # logit = tf.nn.softmax(tf.matmul(fc1,fc2_weights) + fc2_biases)
        
    return logit
