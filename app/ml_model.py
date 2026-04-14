import pickle
import pandas as pd

model = pickle.load(open("ml_models/model.pkl", "rb"))
columns = pickle.load(open("ml_models/columns.pkl", "rb"))

def predict_loan(data):
    
    df = pd.DataFrame([data])

    # Convert categorical to dummy variables
    df = pd.get_dummies(df)

    # Match training columns
    df = df.reindex(columns=columns, fill_value=0)

    # Predict
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return prediction, probability

