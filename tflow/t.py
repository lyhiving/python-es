import tensorflow as tf


sess = tf.Session()

a = tf.constant(1)

b = tf.constant(10)


print(sess.run(a+b))

sess.close()