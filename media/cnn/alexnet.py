from keras.models import Sequential
from keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Flatten, Dropout, Dense
from keras import backend
from keras.constraints import maxnorm


# class PillNet:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def build(width, height, depth, classes):
#         # initialize the model along with the input shape to be
#         # "channels last" and the channels dimension itself
#         input_shape = (height, width, depth)
#         chan_dim = -1
#
#         # if we are using "channels first", update the input shape
#         # and channels dimension
#         if backend.image_data_format() == "channels_first":
#             input_shape = (depth, height, width)
#             chan_dim = 1
#
#         model = Sequential()
#         model.add(Conv2D(32, (3, 3), input_shape=input_shape, activation='relu', padding='same'))
#         model.add(BatchNormalization())  # Using BatchNormalization after activations
#         model.add(Dropout(0.2))
#         model.add(Conv2D(2 * 32, (3, 3), activation='relu', padding='same'))
#         model.add(BatchNormalization())
#         model.add(MaxPooling2D(pool_size=(2, 2)))
#         model.add(Flatten())
#         model.add(Dropout(0.2))
#         model.add(Dense(2000, activation='relu', kernel_constraint=maxnorm(3)))
#         model.add(BatchNormalization())
#         model.add(Dropout(0.5))
#         model.add(Dense(1000, activation='relu', kernel_constraint=maxnorm(3)))
#         model.add(BatchNormalization())
#         model.add(Dropout(0.2))
#         model.add(Dense(classes, activation='softmax'))
#         model.summary()
#         return model
class AlexNet:
    def __init__(self):
        pass

    @staticmethod
    def build(width, height, depth, classes):
        # initialize the model along with the input shape to be
        # "channels last" and the channels dimension itself
        input_shape = (height, width, depth)
        chan_dim = -1

        # if we are using "channels first", update the input shape
        # and channels dimension
        if backend.image_data_format() == "channels_first":
            input_shape = (depth, height, width)
            chan_dim = 1

        model = Sequential()
        model.add(Conv2D(96, (3, 3), input_shape=input_shape, activation='relu', padding='same'))
        model.add(BatchNormalization())  # Using BatchNormalization after activations
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(384, (3, 3), activation='relu', padding='same'))
        model.add(Conv2D(384, (3, 3), activation='relu', padding='same'))
        model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(4096, activation='relu', kernel_constraint=maxnorm(3)))
        # 1
        # model.add(Dropout(0.2))
        # model.add(Dense(2000, activation='relu', kernel_constraint=maxnorm(3)))
        # model.add(Dropout(0.2))
        # model.add(Dense(classes, activation='softmax'))
        # 2
        model.add(Dropout(0.5))
        model.add(Dense(2000, activation='relu', kernel_constraint=maxnorm(3)))
        model.add(Dropout(0.5))
        model.add(Dense(classes, activation='sigmoid'))
        model.summary()
        return model
