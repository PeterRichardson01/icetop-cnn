import tensorflow as tf

# HYBRID0 - SOPHISTICATION OF ADAMW5 WITH SMALLER LAYERS LIKE MINI0
def get_architecture(inputs, prep):

    ## Create convolutional blocks with maxpooling
    conv1 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Conv2D(16, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(inputs['icetop']))
    conv2 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Conv2D(32, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(conv1))
    maxpool1 = tf.keras.layers.MaxPooling2D(pool_size=2, strides=1, padding='same')(conv2)

    conv3 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Conv2D(64, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(maxpool1))
    conv4 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Conv2D(128, kernel_size=3, padding='same', activation='relu', data_format='channels_last')(conv3))
    maxpool2 = tf.keras.layers.MaxPooling2D(pool_size=2, strides=2, padding='same')(conv4)

    ## Prepare flattened input to dense layers
    dense_input = tf.keras.layers.Flatten()(maxpool2)
    if prep['infill']:
        dense_input = tf.keras.layers.Concatenate()([dense_input, tf.keras.layers.Flatten()(inputs['infill'])])
    if prep['reco']:
        dense_input = tf.keras.layers.Concatenate()([dense_input, tf.keras.layers.Flatten()(inputs[prep['reco']])])

    ## Create dense layers with dropout
    dense1 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Dense(128, activation='relu', kernel_constraint=tf.keras.constraints.MaxNorm(3))(dense_input))
    dropout1 = tf.keras.layers.Dropout(1/8)(dense1)
    dense2 = tf.keras.layers.BatchNormalization()(
        tf.keras.layers.Dense(64, activation='relu', kernel_constraint=tf.keras.constraints.MaxNorm(3))(dropout1))
    dropout2 = tf.keras.layers.Dropout(1/8)(dense2)

    ## Create output tensors
    composition_output = tf.keras.layers.Dense(4, activation='softmax', name='comp')(dropout2)
    energy_output = tf.keras.layers.Dense(1, activation='relu', name='energy')(dropout2)

    return [composition_output, energy_output]