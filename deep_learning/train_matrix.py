import os

import numpy as np
import tensorflow as tf
import random
# from tensorflow.examples.tutorials.mnist import input_data

import inference_matrix
# import inference_matrix_2
# print the TC score 
# import print_tc

# SAB_NUM = 423
# BALI_NUM = 180
# OX_NUM = 395

# BATCH_SIZE = 100
FAMILY_NUM = 998
BATCH_SIZE = 40
# BATCH_SIZE = 50
# TRAIN_EXAMPLE_NUM = int(FAMILY_NUM * 0.6)
# train example number is changing all the time.
# data_train = np.load("data_train_np_p_pic_m_pnp.npy")
# data_train = np.load("data_train_np_p_pic_m.npy")
# data_train = np.load("data_train_np_p_pic_m.npy")

# the same data_train, so no need to modify here

# data_train = np.load("data_train_teo_p.npy")
# data_train = np.load("data_train_teo_np.npy")
# data_train = np.load("data_train_teo_pic.npy")
# data_train = np.load("data_train_teo_mafft.npy")

data_train = np.load("data_train.npy")
# data_train = np.load("data_train_uni1_non.npy")

TRAIN_EXAMPLE_NUM = data_train.shape[0]

print TRAIN_EXAMPLE_NUM


# TRAIN_EXAMPLE_NUM = int(FAMILY_NUM * 0.4)
# TRAIN_EXAMPLE_NUM = int(FAMILY_NUM * 0.7)
# TRAIN_EXAMPLE_NUM = int(FAMILY_NUM * 0.8)

# LEARNING_RATE_BASE = 5e-2
# LEARNING_RATE_BASE = 5e-5
# LEARNING_RATE_BASE = 1e-3
LEARNING_RATE_BASE = 3e-4
print ("Learning rate :"),LEARNING_RATE_BASE
# LEARNING_RATE_BASE = 2e-4
# LEARNING_RATE_BASE = 3e-4
# LEARNING_RATE_BASE = 5e-4
# LEARNING_RATE_DECAY = 0.99
# LEARNING_RATE_DECAY = 0.5
LEARNING_RATE_DECAY = 0.99
# LEARNING_RATE_DECAY = 1e-1
REGULARIZATION_RATE = 0.99
# REGULARIZATION_RATE = 1e-1
# TRAINING_STEPS = 800
# TRAINING_STEPS =1600
# TRAINING_STEPS =1301
# TRAINING_STEPS =1600
TRAINING_STEPS = 300
print ("Training steps are :"),TRAINING_STEPS
# TRAINING_STEPS = 950
# TRAINING_STEPS = 1500
# TRAINING_STEPS = 850
# TRAINING_STEPS = 1030
# TRAINING_STEPS = 500
# TRAINING_STEPS = 2500
# TRAINING_STEPS = 3000
MOVING_AVERAGE_DECAY = 0.99
# MOVING_AVERAGE_DECAY = 1e-1

MODEL_SAVE_PATH = "/home/zylu2/tensorflow/pid/CNN/model/4label_random_2_1"

print MODEL_SAVE_PATH
MODEL_NAME = "model.ckpt"

def train(matrix,label):# ,data_all
    # float 32
    # x = tf.placeholder(tf.float32,[BATCH_SIZE,inference_matrix.MATRIX_WIDTH, inference_matrix.MATRIX_LENGTH, inference_matrix.NUM_CHANNELS],name = 'x-input')
    x = tf.placeholder(tf.float32,[BATCH_SIZE,inference_matrix.MATRIX_WIDTH, inference_matrix.MATRIX_LENGTH, inference_matrix.NUM_CHANNELS],name = 'x-input')
    # x = tf.placeholder(tf.float32,[BATCH_SIZE,inference_matrix_2.MATRIX_WIDTH, inference_matrix_2.MATRIX_LENGTH, inference_matrix_2.NUM_CHANNELS],name = 'x-input')
    
    y_ = tf.placeholder(tf.float32,[None,inference_matrix.OUTPUT_NODE],name = 'y-input')
    # y_ = tf.placeholder(tf.float32,[None,inference_matrix_2.OUTPUT_NODE],name = 'y-input')
    
    # y_ = tf.placeholder(tf.float32,[None],name = 'y-input')
    
    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    
    y = inference_matrix.inference(x,True, regularizer)
    
    # y = inference_matrix_2.inference(x,True, regularizer)
    
    global_step = tf.Variable(0,trainable=False)
    
    # loss function, learning rate, average and train
    
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY,global_step)
    
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    
    # cross entropy function  (logits = yPredbyNN, labels=Y)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits = y, labels = tf.argmax(y_,1))
    # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits = y, labels = y_)
    # y_ = tf.nn.softmax(y_)
    # cross_entropy = tf.reduce_mean (tf.square(y_-y))
    # cross_entropy = -tf.reduce_mean (y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    # loss = cross_entropy + tf.add_n(tf.get_collection('losses'))
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    
    # learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE,global_step,mnist.train.num_examples/BATCH_SIZE,LEARNING_RATE_DECAY)
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE,global_step,TRAIN_EXAMPLE_NUM/BATCH_SIZE,LEARNING_RATE_DECAY)
    # train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss,global_step = global_step)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss,global_step = global_step)
    
    with tf.control_dependencies([train_step,variables_averages_op]):
        train_op = tf.no_op(name = 'train')
    
    # initialize the class
    
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
        
        tf.initialize_all_variables().run()
        
        for i in range(TRAINING_STEPS):
            
            # xs,ys = mnist.train.next_batch(BATCH_SIZE)
            start = (i*BATCH_SIZE)% TRAIN_EXAMPLE_NUM
        
            # end = min(start+BATCH_SIZE, TRAIN_EXAMPLE_NUM)
            end = start+BATCH_SIZE
            
            if end <= TRAIN_EXAMPLE_NUM:
                xs = matrix[start:end,:,:,:]
                ys = label[start:end,:]
                shape = ys.shape[1]
                ys = np.reshape(ys,(end-start,shape))# ys, xs shape may not be 20
            else:
                xs = matrix[TRAIN_EXAMPLE_NUM-BATCH_SIZE:TRAIN_EXAMPLE_NUM,:,:,:]
                ys = label[TRAIN_EXAMPLE_NUM-BATCH_SIZE:TRAIN_EXAMPLE_NUM,:]
                shape = ys.shape[1]
                ys = np.reshape(ys,(BATCH_SIZE,shape))# ys, xs shape may not be 20
            
            # ys = label[start:end,:]
            # ys = np.reshape(ys,(end-start,2))# ys, xs shape may not be 20
            # xs reshape
            
            # tf.shape(x)[0]
            # xs = np.reshape(xs,(BATCH_SIZE,inference_matrix.MATRIX_WIDTH,inference_matrix.MATRIX_LENGTH,inference_matrix.NUM_CHANNELS))
            # xs = np.reshape(xs,(tf.shape(xs)[0],inference_matrix.MATRIX_WIDTH,inference_matrix.MATRIX_LENGTH,inference_matrix.NUM_CHANNELS))
            
            # in this way, we can get different input shape, not only a batch, but also the whole data.
            xs = np.reshape(xs,(xs.shape[0],inference_matrix.MATRIX_WIDTH,inference_matrix.MATRIX_LENGTH,inference_matrix.NUM_CHANNELS))
            # xs = np.reshape(xs,(BATCH_SIZE,inference_matrix_2.MATRIX_WIDTH,inference_matrix_2.MATRIX_LENGTH,inference_matrix_2.NUM_CHANNELS))
            
            # x_all = matrix
            _,loss_value, step = sess.run([train_op,loss,global_step], feed_dict = {x:xs, y_:ys})
            
            if i%30 ==0:
                
                
                print ("After %d training steps, loss on training batch is %g."% (step, loss_value))
                # saver.save(sess,os.path.join(MODEL_SAVE_PATH,MODEL_NAME),global_step = global_step)
                # print_tc.print_tc(data_all,MOVING_AVERAGE_DECAY)
                # if i>30 & i%50 ==0:
                    
                    
                    
                
         
        saver.save(sess,os.path.join(MODEL_SAVE_PATH,MODEL_NAME),global_step = global_step)
                
                
def main(argv=None):
        # mnist = input_data.read_data_sets("/tmp/data", one_hot = True)
        # generalize matrices
        # matrix = np.random.rand(inference_matrix.MATRIX_SIZE,inference_matrix.MATRIX_SIZE)
        # read from file
        # data = np.load("998*122*1513*1_mafftAlign.npy")
        # data = np.load("998*122*1513*1_mafftAlign_zero.npy")
        # data = np.load("998*122*1513*1_mafftAlign_zero_nor.npy")
        # data = np.load("998*122*1513*1_mafftAlign_5zero_nor.npy")
        # data = np.load("998*122*1513*1_mafftAlign_5both_zero_nor.npy")
        # data = np.load("998*122*1513*1_mafftAlign_3both_zero_nor.npy")
        # data = np.load("998*122*1513*1_mafftAlign_5both_zero_normalize.npy")
        # data = np.load("998*122*1513*1_mafftAlign_ten_nor.npy")
        # data = np.load("998*122*1513*1_mafftAlign_nor.npy")
        # data = np.load("998*10*500*1_mafftAlign_zero.npy")
        # data = np.load("998*10*500*1_mafftAlign_nor.npy")
        # data = np.load("998*10*500*1_mafftAlign_one.npy")
        # data = np.load("998*10*500*1_mafftAlign_ten.npy")
        # data = np.load("998*8*400*1_mafftAlign_zero.npy")
        # data = np.load("998*5*200*1_mafftAlign_zero.npy")
        # data = np.load("998*5*200*1_mafftAlign_100.npy")
        # data = np.load("998*10*500*1_mafftAlign.npy")
        # randomly load 
        # matrix = matrix[:,:,random]
        
        """rand = np.zeros([1])

        rand_sab = random.sample(range(0,SAB_NUM),int(SAB_NUM*0.6))
        rand_bali = random.sample(range(SAB_NUM,SAB_NUM+BALI_NUM),int(BALI_NUM*0.6))
        rand_ox = random.sample(range(SAB_NUM+BALI_NUM,SAB_NUM+BALI_NUM+OX_NUM),int(OX_NUM*0.6))

        rand_sab = np.array(rand_sab)
        rand_bali = np.array(rand_bali)
        rand_ox = np.array(rand_ox)

        rand = np.hstack([rand,rand_sab])
        rand = np.hstack([rand,rand_bali])
        rand = np.hstack([rand,rand_ox])
        
        rand = rand[1:rand.shape[0]]
        
        rand = rand.astype(int)"""
        
        # rand = random.sample(range(998),TRAIN_EXAMPLE_NUM)
        # rand = np.load("rand_best_f.npy")
        # rand = np.load("rand_best1.npy")
        # np.save("rand",rand)
        
        # rand_rest = []
        # for i in range(998):
            # if i not in rand:
            # print i
                # rand_rest.append(i)
        # rand_rest = np.array(rand_rest)
        # print random.shape
        # np.save("rand_rest",rand_rest)
        
        # data_all = np.load("998*122*1513*1_mafftAlign_5both_zero_nor.npy")
        
        # data_all = data_all.astype(np.float32)
        
        # data_train = np.load("data_train_np_p.npy")
        
        # data_train = np.load("data_train_np_p_pic_m.npy")
        
        # data_train = np.load("data_train_teo_p.npy")
        # data_train = np.load("data_train_teo_np.npy")
        # data_train = np.load("data_train_teo_pic.npy")
        # data_train = np.load("data_train_teo_mafft.npy")
        data_train = np.load("data_train.npy")
        
        # data_train = np.load("data_train_np_p_pic_m_pnp.npy")
        # data_train = np.load("data_train_uni1_non.npy")
        
        print data_train.shape
        
        # data_train = data[rand,:,:,:]
        data_train = data_train.astype(np.float32)
        # matrix = np.load
        # generate labels
        # x = np.array([2,3,1,0])
        
        # labels = np.load("y_train_998*2.npy")
        # labels = np.load("y_train_998*4.npy")
        # labels = np.load("y_train_998*5.npy") y_train_998*4_noPNP
        # labels = np.load("y_train_998*4_noPNP.npy")
        # labels = np.load("y_train_998*4_np_p_pic_m.npy")
        # labels = np.load("y_train_998*4_p_np_pic_m.npy")
        # labels = np.load("y_train_998*5_np_p_pic_m_msa.npy")
        # labels = np.load("y_train_998*5_p_np_pic_m_msa.npy")
        # labels = np.load("y_train_998*3_pic_p_np.npy")
        # labels = np.load("y_train_998*3_p_np_pic.npy")
        # labels = np.load("y_train_998*2_p_np.npy")
        # labels = np.load("y_train_998*4_m_pic_p_np.npy")
        # labels = np.load("y_train_998*4_pic_m_p_np.npy")
        # labels = np.load("y_train_998*4.npy")
        # labels = np.load("y_train_998*4_order.npy")
        
        # label_train = labels[rand]
        
        # label_train = np.load("labels_train_np_p.npy")
        # label_train = np.load("labels_train_np_p_pic_m.npy")
        # labels = np.load("labels_train_teo_p.npy")
        # label_train = np.load("labels_train_uni1_non.npy")
        
        # label_train = np.load("labels_train_np_p_pic_m_pnp.npy")
        
        # label_train = np.load("labels_train_teo_p.npy")
        # label_train = np.load("labels_train_teo_np.npy")
        # label_train = np.load("labels_train_teo_pic.npy")
        # label_train = np.load("labels_train_teo_mafft.npy")
        label_train = np.load("labels_train.npy")
        
        print label_train.shape,label_train[:,0].sum()

        # label_train = np.reshape(label_train,(TRAIN_EXAMPLE_NUM,1))
        # label_train_firstColumn = 1- label_train
        
        # label_train = np.hstack([label_train_firstColumn,label_train])
 
        label_train = label_train.astype(np.float32)
        train(data_train,label_train)
        # train(data_train,label_train,data_all)
        
if __name__ =='__main__':    
    tf.app.run()