from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend

class CNN(object):
    model = None
    img_width = None
    img_height = None
    epochs = None
    batch_size = None

    def __init__(img_width, img_height, epochs, batch_size):
        self.model = Sequential()
        self.img_width = img_width
        self.img_height = img_height
        self.epochs = epochs
        self.batch_size = batch_size
        # Design will be a 3-section embedder
        # with the final section containing the
        # activation function and dropout
        model.add(Conv2D(32, (3,3), input_shape=(3,img_width,img_height)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

    def train(data_dir):
        train_datagen = ImageDataGenerator(rescale=1. /255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        train_generator = train_datagen.flow_from_directory(data_dir, target_size=(self.img_width, self.img_height), batch_size=self.batch_size,class_mode='binary')
        test_datagen = ImageDataGenerator(rescale=1. / 255)

        validation_generator = test_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary')

        model.fit_generator(
            train_generator,
            steps_per_epoch=100,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=100)

        model.save_weights('first_try.h5')
