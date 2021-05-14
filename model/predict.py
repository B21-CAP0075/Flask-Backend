import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


model = tf.keras.models.load_model('model/best_model.h5')
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)


def predict(data):
    patient = data['patient']
    scaler_data = pd.read_csv('model/scaler.csv')

    x = [patient['Age'], patient['EDUC'], patient['SES'], patient['MMSE'], patient['F'], patient['M']]

    scaler = MinMaxScaler().fit(scaler_data.values)
    
    classes = model.predict(scaler.transform([x]))
    
    if classes[0] < 0.5:
        conf = round(float(1.0 - classes[0])*100, 2)
        return f"Normal ({conf}%)"     
    else:
        conf = round(float(classes[0])*100, 2)
        return f"Dementia ({conf}%)"
