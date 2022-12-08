"""
Train:
 > python train.py --dataset C3PI_dataset/train --model pillidentifier.model --labelbin lb.pickle
"""
import argparse
import os
import pickle
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from imutils import paths
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import img_to_array
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from alexnet import AlexNet


def set_keras_backend(backend):
    print("Setting backend")
    if K.backend() != backend:
        print(f"Target backend: {backend}")
        os.environ['KERAS_BACKEND'] = backend
        print("Get backend after reload...")
        print(K.backend())
        assert K.backend() == backend
    if backend == "tensorflow":
        tf.compat.v1.keras.backend.get_session().close()
        cfg = tf.compat.v1.ConfigProto()
        cfg.gpu_options.allow_growth = True
        tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=cfg))
        tf.keras.backend.clear_session()


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True,
                    help="path to input dataset (i.e., directory of images)")
    ap.add_argument("-m", "--model", required=True,
                    help="path to output model")
    ap.add_argument("-l", "--labelbin", required=True,
                    help="path to output label binarizer")
    ap.add_argument("-p", "--plot", type=str, default="plot.png",
                    help="path to output accuracy/loss plot")
    args = vars(ap.parse_args())

    return args


def print_history_accuracy(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def print_history_loss(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def load_dataset(img_dims):
    args = get_arguments()
    # initialize the image dimensions
    data = []
    labels = []

    # Shuffle data.
    print("[INFO] loading images...")
    image_paths = sorted(list(paths.list_images(args["dataset"])))
    print(image_paths)
    random.seed(42)
    random.shuffle(image_paths)

    # loop over the input images
    for image_path in image_paths:
        # load the image, pre-process it, and store it in the data list.
        print(image_path)
        image = cv2.imread(image_path)
        image = cv2.resize(image, (img_dims[1], img_dims[0]))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the
        # labels list
        label = image_path.split(os.path.sep)[-2]
        labels.append(label)

        # Scale the raw pixel intensities to the range [0, 1].
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)
    print("[INFO] data matrix: {:.2f}MB".format(
        data.nbytes / (1024 * 1000.0)))

    # Binarize the labels.
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)

    # 80% for training, 20% for validation.
    train_x, test_x, train_y, test_y = train_test_split(data, labels, test_size=0.2, random_state=42)

    return train_x, test_x, train_y, test_y, lb


def compile_train_model(data_augmentation):
    args = get_arguments()

    """
    Hyperparameters
    - Tweak these values according to your needs.
    - If you get a OOM error you should check if you are using a GPU, 
      otherwise you should lower these values so you can allocate enough 
      resources for the model to be trained (reducing batch size, for example).
    """
    EPOCHS = 150
    INIT_LR = 2e-5
    BS = 32
    IMAGE_DIMS = (96, 96, 3)
    train_x, test_x, train_y, test_y, lb = load_dataset(IMAGE_DIMS)

    # Initialize the model.
    print("[INFO] compiling model...")
    model = AlexNet.build(width=IMAGE_DIMS[1],
                          height=IMAGE_DIMS[0],
                          depth=IMAGE_DIMS[2],
                          classes=len(lb.classes_))

    opt = Adam(lr=INIT_LR,
               decay=INIT_LR / EPOCHS)

    model.compile(loss="categorical_crossentropy",
                  optimizer=opt,
                  metrics=["accuracy"])

    tensorboard = TensorBoard(log_dir='log/', histogram_freq=0,
                              write_graph=True, write_images=False)

    if not data_augmentation:
        print('Not using data augmentation.')
        print("[INFO] training network...")
        hist = model.fit(train_x, train_y,
                         batch_size=BS,
                         epochs=EPOCHS,
                         validation_data=(test_x, test_y),
                         callbacks=[tensorboard],
                         shuffle=True)
    else:
        print('Using real-time data augmentation.')

        # Create real-time image data augmentation generator
        datagen = ImageDataGenerator(rotation_range=25,
                                     width_shift_range=0.1,
                                     height_shift_range=0.1,
                                     shear_range=0.2,
                                     zoom_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode="nearest")

        print("[INFO] training network...")

        # Fit the model on the batches generated by datagen.flow().
        hist = model.fit(datagen.flow(train_x,
                                      train_y,
                                      batch_size=BS,
                                      ),
                         validation_data=(test_x, test_y),
                         steps_per_epoch=train_x.shape[0] // BS,
                         epochs=EPOCHS,
                         verbose=1,
                         callbacks=[tensorboard],
                         )

    print_history_accuracy(hist)
    print_history_loss(hist)

    # Save the model to disk
    print("[INFO] serializing network...")
    model.save(args["model"])

    # Save the label binarizer to disk
    print("[INFO] serializing label binarizer...")
    f = open(args["labelbin"], "wb")
    f.write(pickle.dumps(lb))
    f.close()

    # Evaluation
    scores = model.evaluate(test_x, test_y, verbose=1)
    print('Scores:  ', scores)
    print("Accuracy:    %.2f%%" % (scores[1] * 100))
    print("Model Error:    %.2f%%" % (100 - scores[1] * 100))


if __name__ == "__main__":
    print("Setting Keras backend...")
    set_keras_backend("tensorflow")
    args = get_arguments()
    compile_train_model(data_augmentation=True)
