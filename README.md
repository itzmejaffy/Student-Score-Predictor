🎓 Student Score Predictor

An AI-powered Machine Learning web application that predicts students’ academic performance based on study hours, attendance, and previous marks.

✨ Features

* Predict student scores using Machine Learning.
* Input study hours, attendance, and previous marks.
* Interactive web interface built with Streamlit.
* Fast prediction API using FastAPI.
* Data visualization using Plotly.

🛠️ Technologies Used

* Python
* Machine Learning (Scikit-learn)
* Pandas & NumPy
* FastAPI
* Streamlit
* Plotly

📁 Project Structure

Student-Score-Predictor/
│
├── backend/
│   ├── main.py
│   └── model.py
│
├── frontend/
│   └── app.py
│
├── dataset/
│   └── students.csv
│
├── requirements.txt
└── README.md

🚀 How to Run

1. Clone the repository

git clone https://github.com/itzmejaffy/Student-Score-Predictor.git
cd Student-Score-Predictor

2. Install dependencies

pip install -r requirements.txt

3. Start the backend

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

4. Start the frontend

Open another terminal:

streamlit run frontend/app.py

🎯 Project Goal

To demonstrate how Machine Learning can be used to estimate student academic performance through simple input features.

👩‍💻 Author

Jaffy

GitHub: @itzmejaffy
## Website Preview

![Student Score Predictor](screenshots/website-23mb.jpeg)
