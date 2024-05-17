from flask import Flask, render_template, request
from joblib import load
import pandas as pd

app = Flask(__name__)

# Load the trained model from the pickle file
loaded_model = load('random_forest_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Print form data for debugging
    print(request.form)

    # Ensure all required fields are filled in
    required_fields = ['duration', 'protocol_type', 'service', 'src_bytes', 'dst_bytes',
                       'count', 'srv_count', 'serror_rate', 'srv_serror_rate']

    for field in required_fields:
        if field not in request.form or not request.form[field]:
            return render_template('error.html', message=f'Field "{field}" is required.')

    # Extract network properties from the form
    try:
        features = [
            float(request.form['duration']),
            float(request.form['protocol_type']),
            float(request.form['service']),
            float(request.form['src_bytes']),
            float(request.form['dst_bytes']),
            float(request.form['count']),
            float(request.form['srv_count']),
            float(request.form['serror_rate']),
            float(request.form['srv_serror_rate'])
        ]
    except ValueError as e:
        return render_template('error.html', message=f'Error converting input to float: {e}')
    except KeyError as e:
        return render_template('error.html', message=f'Missing required field: {e}')

    # Create a DataFrame with the input features
    input_data = pd.DataFrame([features])

    # Make a prediction using the loaded model
    prediction = loaded_model.predict(input_data)[0]

    # Determine if there is an anomaly or not
    result = 'Anomaly Detected' if prediction == 1 else 'No Anomaly Detected'

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
