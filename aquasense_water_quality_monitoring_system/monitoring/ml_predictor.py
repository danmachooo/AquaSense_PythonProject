import joblib
import pandas as pd


# Load the pre-trained model
model = joblib.load('../models/Trained/mdmc_modelv5.2.joblib')

# Define the feature names used during model training
feature_names = [
    'pH', 'Temperature', 'Dissolved Oxygen', 'Electrical Conductivity',
    'Turbidity', 'Nitrogen', 'Phosphorus', 'Potassium', 
    'Water Hardness', 'pH_squared', 'DO_EC_ratio', 'NPK_sum'
]

def predict_water_quality(data):
    # Prepare the input data
    data['pH_squared'] = data['pH'] ** 2
    data['DO_EC_ratio'] = data['Dissolved Oxygen'] / data['Electrical Conductivity']
    data['NPK_sum'] = data['Nitrogen'] + data['Phosphorus'] + data['Potassium']

    input_data = [
        data['pH'], data['Temperature'], data['Dissolved Oxygen'], data['Electrical Conductivity'],
        data['Turbidity'], data['Nitrogen'], data['Phosphorus'],
        data['Potassium'], data['Water Hardness'], data['pH_squared'], data['DO_EC_ratio'], data['NPK_sum']
    ]

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data], columns=feature_names)

    # Make prediction
    prediction = model.predict(input_df)[0]
    
    return prediction
