from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_score

app = FastAPI(title="Student Score Predictor API")


class StudentData(BaseModel):
    study_hours: float
    attendance: float
    previous_marks: float


@app.get("/")
def home():
    return {"message": "Student Score Predictor API is running!"}


@app.post("/predict")
def predict(data: StudentData):

    score = predict_score(
        data.study_hours,
        data.attendance,
        data.previous_marks
    )

    return {
        "predicted_score": score,
        "message": "Prediction successful!"
    }