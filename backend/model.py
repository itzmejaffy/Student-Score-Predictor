import pandas as pd
from sklearn.linear_model import LinearRegression

# Sample student dataset
data = {
    "study_hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "attendance": [50, 55, 60, 65, 70, 75, 80, 85, 90, 95],
    "previous_marks": [40, 45, 50, 55, 60, 65, 70, 75, 80, 85],
    "score": [35, 40, 48, 53, 60, 68, 74, 82, 89, 96]
}

df = pd.DataFrame(data)

# Input features
X = df[["study_hours", "attendance", "previous_marks"]]

# Target variable
y = df["score"]

# Train model
model = LinearRegression()
model.fit(X, y)


def predict_score(study_hours, attendance, previous_marks):

    prediction = model.predict([[
        study_hours,
        attendance,
        previous_marks
    ]])

    return round(float(prediction[0]), 2)