from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/')
def index():
    return 'Hello Cloud Run!'


@app.route('/predict', methods=['POST'])
def get_prediction():
    json = request.get_json()
    print(json)
    
    if json is None:
        return jsonify({'error': 'invalid input'})

    prediction, confident = predict.predict(json)
    return jsonify({'prediction': prediction, 'confident': confident})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)