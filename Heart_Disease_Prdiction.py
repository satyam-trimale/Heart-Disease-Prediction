import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Feature names (assuming you have them)
feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

# Feature names and their descriptive labels
feature_labels = {
    'age': 'Age',
    'sex': 'Sex',
    'cp': 'Chest Pain Type',
    'trestbps': 'Resting Blood Pressure',
    'chol': 'Serum Cholestoral in mg/dl',
    'fbs': 'Fasting Blood Sugar > 120 mg/dl',
    'restecg': 'Resting Electrocardiographic Results',
    'thalach': 'Maximum Heart Rate Achieved',
    'exang': 'Exercise Induced Angina',
    'oldpeak': 'ST Depression Induced by Exercise Relative to Rest',
    'slope': 'The Slope of the Peak Exercise ST Segment',
    'ca': 'Number of Major Vessels (0-3) Colored by Flourosopy',
    'thal': 'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect'
}

# Feature options for selectboxes
feature_options = {
    'sex': ['Male', 'Female'],
    'cp': ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic'],
    'fbs': ['False', 'True'],
    'restecg': ['Normal', 'Having ST-T wave abnormality', 'Showing probable or definite left ventricular hypertrophy by Estes criteria'],
    'exang': ['No', 'Yes'],
    'slope': ['Upsloping', 'Flat', 'Downsloping'],
    'thal': ['Normal', 'Fixed defect', 'Reversable defect'] 
}

# Create the Streamlit app
st.title("Heart Disease Prediction")
# Input fields for user data
input_data = []
for i, feature in enumerate(feature_names):
    if feature in feature_options:
        user_input = st.selectbox(feature_labels[feature], options=feature_options[feature], key=f"{feature}_selectbox")
        
        # Convert user input to numerical value if needed
        if feature == 'sex':
            input_data.append(0 if user_input == 'Female' else 1)  
        elif feature in ['cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']:
            input_data.append(feature_options[feature].index(user_input))  # Get index of selected option
        else:
            input_data.append(user_input)  # For other selectboxes, keep as is
    else:
        if feature == 'oldpeak':  # Check for 'oldpeak'
            input_data.append(st.number_input(feature_labels[feature], value=0.0, step=0.1, key=f"{feature}_{i}"))  # Added step=0.1
        else:
            input_data.append(st.number_input(feature_labels[feature], value=0, key=f"{feature}_{i}"))

# Convert input data to DataFrame
input_data_df = pd.DataFrame([input_data], columns=feature_names)

# Make prediction
if st.button("Predict"):
    prediction = model.predict(input_data_df)
    if prediction[0] == 0:
        st.success("The Person does not have a Heart Disease")
    else:
        st.error("The Person has Heart Disease")