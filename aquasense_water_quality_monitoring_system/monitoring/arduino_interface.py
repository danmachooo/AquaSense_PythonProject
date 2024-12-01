import serial
import json
from .models import WaterQualityReading
from .ml_predictor import predict_water_quality

def read_arduino_data():
    ser = serial.Serial('COM3', 9600)  # Adjust port as needed
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = json.loads(line)
            
            # Predict water quality
            label = predict_water_quality(data)
            
            # Save to database
            WaterQualityReading.objects.create(
                pH=data['pH'],
                temp=data['Temperature'],
                DO=data['Dissolved Oxygen'],
                EC=data['Electrical Conductivity'],
                turbidity=data['Turbidity'],
                nitrogen=data['Nitrogen'],
                phosphorus=data['Phosphorus'],
                potassium=data['Potassium'],
                hardness=data['Water Hardness'],
                label=int(label)
            )

            print(f"Saved label: {label}")