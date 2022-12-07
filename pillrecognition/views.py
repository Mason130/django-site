from keras.models import load_model
from keras.utils import img_to_array
import pickle
import cv2
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from .models import PillsInformation, UploadImage
from .forms import UploadImageForm
from django.conf import settings


def identify(img_path):
    # MODEL_PATH = 'cnn/pillidentifier.model'
    MODEL_PATH = settings.MEDIA_ROOT + 'cnn/pillidentifier.model'
    model = load_model(MODEL_PATH)
    lb = pickle.loads(open(settings.MEDIA_ROOT + 'cnn/lb.pickle', "rb").read())
    img = cv2.imread(img_path)
    img = cv2.resize(img, (96, 96))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    # Predicting the label of the input image.
    print("[INFO] classifying image...")
    proba = model.predict(img)[0]
    idx = np.argmax(proba)
    print(proba[idx])
    label = lb.classes_[idx]
    return round(proba[idx]*100, 2), int(label)


def pill_recognition_view(request):
    image = UploadImage.objects.get_or_create()
    image = UploadImage.objects.get(id=1)
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            pill = UploadImage.objects.get(id=1)
            path = settings.MEDIA_ROOT + str(pill.pill_image)
            probability, pill_number = identify(path)
            information = PillsInformation.objects.get(id=pill_number)
            return render(request, 'pillrecognition/results.html', {'pill': pill,
                                                                    'information': information,
                                                                    'probability': probability})
        else:
            return HttpResponse("Invalid image")
    else:
        form = UploadImageForm()
    return render(request, 'pillrecognition/identification.html', {'form': form, })


def results_view(request):
    return render(request, 'pillrecognition/results.html')
