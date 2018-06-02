from keras.layers import Input, Dense, Embedding, Conv2D, MaxPool1D, Conv1D, Convolution2D
from keras.layers import Reshape, Flatten, Dropout, Concatenate
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.models import Model, Sequential
from sklearn.model_selection import train_test_split
from data_helpers import load_data
from livelossplot import PlotLossesKeras
from matplotlib import pyplot


print('Loading data')
x, y, max_sentace_length=  load_data()
# x, y, vocabulary, vocabulary_inv = load_data()
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# X_train.shape -> (44958, 220)
# y_train.shape -> (44958, 1)
# X_test.shape -> (9992, 220)
# y_test.shape -> (9992, 1)



# X_train.shape -> (8529, 56)
# y_train.shape -> (8529, 2)
# X_test.shape -> (2133, 56)
# y_test.shape -> (2133, 2)


sequence_length = (max_sentace_length, 100) # number of signs in sentace
#vocabulary_size = X_test.max()
embedding_dim = 256
filter_sizes = [3,4,5]
num_filters = 512
drop = 0.5

epochs = 40
batch_size = 30

# this returns a tensor
print("Creating Model...")
inputs = Input(shape=(sequence_length), dtype='float32')
# embedding = Embedding(input_dim=vocabulary_size, output_dim=embedding_dim, input_length=sequence_length)(inputs)
#reshape = Reshape((sequence_length,embedding_dim,1))(input)




conv_0 = Conv1D(num_filters, kernel_size=(filter_sizes[0]), padding='valid', kernel_initializer='normal', activation='relu')(inputs)
conv_1 = Conv1D(num_filters, kernel_size=(filter_sizes[1]), padding='valid', kernel_initializer='normal', activation='relu')(inputs)
conv_2 = Conv1D(num_filters, kernel_size=(filter_sizes[2]), padding='valid', kernel_initializer='normal', activation='relu')(inputs)

maxpool_0 = MaxPool1D(pool_size=(2), strides=1, padding='valid')(conv_0)
maxpool_1 = MaxPool1D(pool_size=(2), strides=1, padding='valid')(conv_1)
maxpool_2 = MaxPool1D(pool_size=(2), strides=1, padding='valid')(conv_2)

concatenated_tensor = Concatenate(axis=1)([ maxpool_1, maxpool_2])
flatten = Flatten()(concatenated_tensor)
dropout = Dropout(drop)(flatten)
output = Dense(units=2, activation='softmax')(dropout)

# this creates a model that includes
model = Model(inputs=inputs, outputs=output)

checkpoint = ModelCheckpoint('weights.{epoch:03d}-{val_acc:.4f}.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto')
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())

print("Traning Model...")

history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=[checkpoint], validation_data=(X_test, y_test))  # starts training
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model train vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'validation'], loc='upper right')
pyplot.show()
pyplot.plot(history.history['acc'])
pyplot.plot(history.history['val_acc'])
pyplot.title('model accuracy')
pyplot.ylabel('accuracy')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'test'], loc='upper left')
pyplot.show()