
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="StudentIQ | Academic Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/predict"

# ==========================================
# SESSION STATE
# ==========================================

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F7F9FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    color: #172B4D;
}

p {
    color: #526078;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8EDF5;
}

[data-testid="stSidebar"] h1 {
    color: #3978F6;
}

.metric-card {
    background-color: white;
    border: 1px solid #E5EAF2;
    border-radius: 14px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(20,40,80,0.04);
}

.metric-title {
    color: #718096;
    font-size: 14px;
}

.metric-value {
    color: #172B4D;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
}

.metric-description {
    color: #94A3B8;
    font-size: 12px;
}

.section-subtitle {
    color: #718096;
    font-size: 15px;
}

div.stButton > button {
    background-color: #3978F6;
    color: white;
    border-radius: 9px;
    border: none;
    min-height: 43px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #245ED0;
    color: white;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border: 1px solid #E5EAF2;
    border-radius: 12px;
}

hr {
    border-color: #E5EAF2;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# REUSABLE FUNCTIONS
# ==========================================

def metric_card(title, value, description):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title, subtitle):
    st.title(title)
    st.markdown(
        f'<p class="section-subtitle">{subtitle}</p>',
        unsafe_allow_html=True
    )
    st.divider()


def get_recommendations(study_hours, attendance, previous_marks):

    recommendations = []

    if study_hours < 3:
        recommendations.append(
            "Try studying for at least 3 hours daily. "
            "Build a consistent study schedule."
        )
    else:
        recommendations.append(
            "Good study routine! Maintain consistency "
            "and revise regularly."
        )

    if attendance < 75:
        recommendations.append(
            "Your attendance is relatively low. "
            "Attend more classes to avoid missing important topics."
        )
    else:
        recommendations.append(
            "Your attendance is looking good. "
            "Continue participating in classes."
        )

    if previous_marks < 50:
        recommendations.append(
            "Focus on strengthening your fundamentals "
            "and practise basic questions."
        )
    elif previous_marks < 75:
        recommendations.append(
            "Work on improving your accuracy through "
            "regular practice tests."
        )
    else:
        recommendations.append(
            "Your previous marks are strong. "
            "Challenge yourself with advanced questions."
        )

    return recommendations


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.title("🎓 StudentIQ")

    st.caption("AI Academic Insights")

    st.divider()

    st.markdown("### NAVIGATION")

    selected_page = st.radio(
        "Navigate",
        [
            "Dashboard",
            "Score Predictor",
            "Performance Analytics",
            "Study Recommendations",
            "About Project"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### PROJECT STATUS")

    st.success("Frontend Active")

    st.caption("Powered by Streamlit + FastAPI")

    st.divider()

    st.caption("StudentIQ | Machine Learning Project")


# ==========================================
# PAGE 1: DASHBOARD
# ==========================================

if selected_page == "Dashboard":

    page_header(
        "Welcome to StudentIQ 👋",
        "Your academic performance prediction and analysis dashboard."
    )

    st.subheader("Your Academic Overview")

    total_predictions = len(
        st.session_state.prediction_history
    )

    latest_prediction = st.session_state.last_prediction

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "TOTAL PREDICTIONS",
            total_predictions,
            "Predictions in this session"
        )

    with col2:
        if latest_prediction:
            metric_card(
                "LATEST PREDICTED SCORE",
                f"{latest_prediction['score']}/100",
                "Most recent prediction"
            )
        else:
            metric_card(
                "LATEST PREDICTED SCORE",
                "--",
                "No prediction yet"
            )

    with col3:
        metric_card(
            "ML ALGORITHM",
            "Linear Regression",
            "Machine Learning Model"
        )

    st.write("")

    st.subheader("Explore StudentIQ")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Score Predictor")
            st.write(
                "Enter study hours, attendance and previous marks "
                "to predict your exam score."
            )

            st.info("Use Score Predictor in the sidebar to begin.")

    with col2:
        with st.container(border=True):
            st.markdown("### 📈 Performance Analytics")
            st.write(
                "View your previous predictions and understand "
                "your academic performance."
            )

            st.info(
                "Your prediction history will appear in Analytics."
            )

    st.write("")

    with st.container(border=True):
        st.markdown("### 🤖 How StudentIQ Works")

        st.write(
            "StudentIQ uses a Machine Learning model to estimate "
            "exam performance based on three academic factors."
        )

        a, b, c = st.columns(3)

        with a:
            st.markdown("**📚 Study Hours**")
            st.caption("Daily time spent studying")

        with b:
            st.markdown("**📅 Attendance**")
            st.caption("Student attendance percentage")

        with c:
            st.markdown("**📝 Previous Marks**")
            st.caption("Previous examination performance")


# ==========================================
# PAGE 2: SCORE PREDICTOR
# ==========================================

elif selected_page == "Score Predictor":

    page_header(
        "Student Score Predictor",
        "Enter academic information to estimate your examination score."
    )

    left, right = st.columns([1, 1], gap="large")

    with left:

        with st.container(border=True):

            st.subheader("📋 Student Information")

            with st.form("prediction_form"):

                study_hours = st.number_input(
                    "Daily Study Hours",
                    min_value=0.0,
                    max_value=24.0,
                    value=5.0,
                    step=0.5
                )

                attendance = st.number_input(
                    "Attendance Percentage",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    step=1.0
                )

                previous_marks = st.number_input(
                    "Previous Exam Marks",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0,
                    step=1.0
                )

                submitted = st.form_submit_button(
                    "✨ Predict My Score",
                    use_container_width=True
                )

    with right:

        with st.container(border=True):

            st.subheader("🎯 Prediction Results")

            if submitted:

                payload = {
                    "study_hours": study_hours,
                    "attendance": attendance,
                    "previous_marks": previous_marks
                }

                try:

                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=10
                    )

                    response.raise_for_status()

                    result = response.json()

                    score = float(result["predicted_score"])

                    if not 0 <= score <= 100:
                        st.warning(
                            f"The model returned {score:.2f}. "
                            "This is outside the expected 0–100 range."
                        )

                    else:

                        st.session_state.last_prediction = {
                            "score": score,
                            "study_hours": study_hours,
                            "attendance": attendance,
                            "previous_marks": previous_marks
                        }

                        st.session_state.prediction_history.append({
                            "Prediction": len(
                                st.session_state.prediction_history
                            ) + 1,
                            "Study Hours": study_hours,
                            "Attendance": attendance,
                            "Previous Marks": previous_marks,
                            "Predicted Score": score
                        })

                        st.success("Prediction generated successfully!")

                        st.metric(
                            "Predicted Examination Score",
                            f"{score:.2f}/100"
                        )

                        fig = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=score,
                                number={"suffix": "%"},
                                title={
                                    "text": "Predicted Performance"
                                },
                                gauge={
                                    "axis": {
                                        "range": [0, 100]
                                    },
                                    "bar": {
                                        "color": "#3978F6"
                                    },
                                    "bgcolor": "#EAF0FA",
                                    "steps": [
                                        {
                                            "range": [0, 40],
                                            "color": "#FDE8E8"
                                        },
                                        {
                                            "range": [40, 70],
                                            "color": "#FFF3D6"
                                        },
                                        {
                                            "range": [70, 100],
                                            "color": "#DDF5E7"
                                        }
                                    ]
                                }
                            )
                        )

                        fig.update_layout(
                            height=280,
                            margin=dict(
                                l=20, r=20, t=50, b=10
                            ),
                            paper_bgcolor="white"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                        st.caption(
                            "This is an estimate from a small "
                            "illustrative dataset, not a guaranteed result."
                        )

                except requests.exceptions.RequestException:

                    st.error(
                        "Cannot connect to the backend. "
                        "Please make sure FastAPI is running."
                    )

                except (KeyError, ValueError, TypeError):

                    st.error(
                        "Unexpected response received from the backend."
                    )

            else:

                st.info(
                    "Your predicted score will appear here "
                    "after submitting your academic information."
                )

    # Latest prediction details

    if st.session_state.last_prediction:

        st.write("")

        st.subheader("Latest Prediction Details")

        latest = st.session_state.last_prediction

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Study Hours",
                f"{latest['study_hours']} hrs"
            )

        with b:
            st.metric(
                "Attendance",
                f"{latest['attendance']}%"
            )

        with c:
            st.metric(
                "Previous Marks",
                f"{latest['previous_marks']}/100"
            )


# ==========================================
# PAGE 3: PERFORMANCE ANALYTICS
# ==========================================

elif selected_page == "Performance Analytics":

    page_header(
        "Performance Analytics 📊",
        "Explore your prediction history and academic indicators."
    )

    history = st.session_state.prediction_history

    if not history:

        st.info(
            "No prediction history available yet. "
            "Go to Score Predictor and generate your first prediction."
        )

    else:

        df = pd.DataFrame(history)

        avg_score = df["Predicted Score"].mean()

        best_score = df["Predicted Score"].max()

        col1, col2, col3 = st.columns(3)

        with col1:
            metric_card(
                "AVERAGE PREDICTION",
                f"{avg_score:.2f}",
                "Across this session"
            )

        with col2:
            metric_card(
                "HIGHEST PREDICTION",
                f"{best_score:.2f}",
                "Best predicted score"
            )

        with col3:
            metric_card(
                "TOTAL PREDICTIONS",
                len(df),
                "Recorded this session"
            )

        st.write("")

        st.subheader("Prediction History")

        fig = px.line(
            df,
            x="Prediction",
            y="Predicted Score",
            markers=True,
            title="Predicted Score Trend"
        )

        fig.update_traces(
            line=dict(color="#3978F6", width=3),
            marker=dict(size=9)
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Prediction Number",
            yaxis_title="Predicted Score",
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Academic Input Comparison")

        comparison = df.melt(
            id_vars=["Prediction"],
            value_vars=[
                "Study Hours",
                "Attendance",
                "Previous Marks"
            ],
            var_name="Academic Factor",
            value_name="Value"
        )

        fig2 = px.bar(
            comparison,
            x="Academic Factor",
            y="Value",
            color="Academic Factor",
            barmode="group",
            title="Academic Factors Across Predictions"
        )

        fig2.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.subheader("Prediction Records")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ==========================================
# PAGE 4: STUDY RECOMMENDATIONS
# ==========================================

elif selected_page == "Study Recommendations":

    page_header(
        "Study Recommendations 💡",
        "Get simple academic suggestions based on your latest inputs."
    )

    latest = st.session_state.last_prediction

    if latest is None:

        st.info(
            "Generate a prediction first. "
            "Your study recommendations will appear here."
        )

    else:

        st.subheader("Your Academic Insights")

        recommendations = get_recommendations(
            latest["study_hours"],
            latest["attendance"],
            latest["previous_marks"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Study Hours",
                f"{latest['study_hours']} hrs/day"
            )

            st.metric(
                "Attendance",
                f"{latest['attendance']}%"
            )

        with col2:

            st.metric(
                "Previous Marks",
                f"{latest['previous_marks']}/100"
            )

            st.metric(
                "Predicted Score",
                f"{latest['score']:.2f}/100"
            )

        st.divider()

        st.subheader("Personalized Suggestions")

        for i, recommendation in enumerate(
            recommendations, start=1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**{i}. {recommendation}**"
                )

        st.caption(
            "These are general study suggestions based on "
            "your entered information, not a validated AI diagnosis."
        )


# ==========================================
# PAGE 5: ABOUT PROJECT
# ==========================================

elif selected_page == "About Project":

    page_header(
        "About StudentIQ 🎓",
        "Learn about the project, technologies and machine learning approach."
    )

    with st.container(border=True):

        st.subheader("Project Overview")

        st.write(
            "StudentIQ is a Student Score Prediction application "
            "that estimates academic performance using Machine Learning."
        )

        st.write(
            "Students provide study hours, attendance percentage "
            "and previous examination marks. The application sends "
            "these details to a FastAPI backend, which returns "
            "a predicted score."
        )

    st.write("")

    st.subheader("Technologies Used")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### 🐍 Python")
            st.write("Main programming language.")

            st.markdown("### 🤖 Scikit-learn")
            st.write("Machine Learning model training.")

            st.markdown("### 🐼 Pandas")
            st.write("Data handling and analysis.")

    with col2:

        with st.container(border=True):

            st.markdown("### ⚡ FastAPI")
            st.write("Backend API and prediction endpoint.")

            st.markdown("### 🎨 Streamlit")
            st.write("Interactive frontend dashboard.")

            st.markdown("### 📊 Plotly")
            st.write("Interactive charts and visualizations.")

    st.write("")

    st.subheader("Machine Learning Model")

    with st.container(border=True):

        st.write(
            "**Algorithm:** Linear Regression"
        )

        st.write(
            "**Input Features:** Study Hours, Attendance, Previous Marks"
        )

        st.write(
            "**Output:** Predicted Examination Score"
        )

        st.caption(
            "The current model uses a small illustrative dataset. "
            "Its predictions are for demonstration purposes and "
            "should not be treated as reliable academic forecasts."
        )

    st.divider()

    st.subheader("Project Developer")

    st.markdown("### 👩‍💻 Jaffy J")

    st.write(
        "B.E. Computer Science and Engineering – "
        "Artificial Intelligence and Machine Learning"
    )

    st.caption("StudentIQ | Machine Learning Project")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#94A3B8; padding:10px;">
        StudentIQ | Built with Python, Streamlit and Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
