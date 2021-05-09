import tensorflow as tf
import base64
import io
import numpy as np
from PIL import Image
from keras.preprocessing import image

model = tf.keras.models.load_model('model/model.h5')
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

def preprocess_image(img, target_size):
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img = img.resize(target_size)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255
    return img

def predict(data):
    img = Image.open(data)
    processed_image = preprocess_image(img, target_size=(150, 150))

    images = np.vstack([processed_image])
    classes = model.predict(images, batch_size=10)
    label = np.where(classes[0] > 0.5, 1,0)
    if label == 0:
        conf = round(float(1.0 - classes[0])*100, 2)
        return f"Fresh Fruit ({conf}%)"    
    else:
        conf = round(float(classes[0])*100, 2)
        return f"Rotten Fruit ({conf}%)"
