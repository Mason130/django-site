from keras.models import load_model
from keras.utils import img_to_array
import pickle
import cv2
import numpy as np
import psycopg2
import tensorflow as tf


# Connect to database
conn = psycopg2.connect(database="postgres",
                        host="database-1.ciwtxtgqt2xy.us-east-2.rds.amazonaws.com",
                        user="postgres",
                        password="Yc1009917006",
                        port="5432")
cursor = conn.cursor()

# Create your views here.
MODEL_PATH = 'pillidentifier.model'
model = load_model(MODEL_PATH)
tf.keras.utils.plot_model(
    model,
    to_file='model.png',
    show_shapes=True,
    show_dtype=False,
    show_layer_names=False,
    show_layer_activations=True,
    dpi=100
)
lb = pickle.loads(open('lb.pickle', "rb").read())
img_path = "C3PI_dataset/train/6/1066.jpg"
img = cv2.imread(img_path)
img = cv2.resize(img, (96, 96))
img = img.astype("float") / 255.0
img = img_to_array(img)
img = np.expand_dims(img, axis=0)

# Predicting the label of the input image.
print("[INFO] classifying image...")
proba = model.predict(img)[0]
print(proba)
idx = np.argmax(proba)
label = lb.classes_[idx]
cursor.execute("SELECT * FROM pillrecognition_pillsinformation WHERE id=%s", (label,))
rows = cursor.fetchall()
print(rows)

print(f"Printing label: {label}")
new_label = "{}: {:.2f}%".format(label, proba[idx] * 100)
print(f"Printing new label: {new_label}")

# Prediction probability.
prob = proba[idx] * 100
print("Probability: {:.2f}%".format(prob))
# data["probability"] = prob
