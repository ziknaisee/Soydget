
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SOYDGET AI", page_icon="🌱", layout="wide")

MODULES = {
    "1. Introduction": "Okara, Soydget concept, learning outcomes and the role of Human-AI collaboration.",
    "2. Halal Food": "Halal critical points, ingredient sourcing, hygiene and safety considerations.",
    "3. Food Sustainability": "Okara upcycling, circular food economy and sustainability awareness.",
    "4. Food Innovation": "Formulation concepts, mass balance, ingredient substitution and product innovation.",
    "5. Soydget Formulation": "Digital formulation, AI prediction and preparation for physical laboratory validation.",
}

if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "sensory" not in st.session_state:
    st.session_state.sensory = None

def predict(okara, binder, flour, water, oil, seasoning):
    # DEMO logic only. Replace with a validated ML model using the project's real dataset.
    moisture = np.clip(52 + 0.32*okara + 0.22*water - 0.12*flour, 0, 100)
    texture = np.clip(5.2 + 0.06*binder + 0.035*flour - 0.025*okara + 0.015*oil, 1, 9)
    aroma = np.clip(5.8 + 0.025*seasoning + 0.01*oil - 0.008*okara, 1, 9)
    acceptability = np.clip(0.35*texture + 0.30*aroma + 2.0, 1, 9)
    return moisture, texture, aroma, acceptability

def sidebar():
    st.sidebar.title("🌱 SOYDGET AI")
    st.sidebar.caption("Human-AI Collaborative Learning Platform")
    role = st.sidebar.radio("Mode", ["Student", "Lecturer"])
    st.sidebar.divider()
    st.sidebar.info("NALI 2026 Prototype\nDigitalising Okara Nugget (Soydget) Innovation")
    return role

role = sidebar()

st.title("🌱 SOYDGET AI")
st.caption("Predict Digitally • Validate Physically • Learn Collaboratively")

if role == "Student":
    tabs = st.tabs(["🏠 Home", "📚 Learning Modules", "🤖 AI Formulation", "🧪 Sensory Validation"])

    with tabs[0]:
        st.subheader("Human-AI Collaborative Learning Journey")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Modules", "5")
        c2.metric("AI Simulation", "Ready")
        c3.metric("Sensory Scale", "9-point")
        c4.metric("Validation", "Closed-loop")
        st.markdown("""
        **Learning flow**

        `Learn → Simulate → Predict → Physical Lab → Validate → Reflect`

        The AI supports formulation decisions; students remain responsible for interpreting
        and validating the prediction through laboratory evidence.
        """)

    with tabs[1]:
        st.subheader("Five Core Learning Modules")
        for name, desc in MODULES.items():
            with st.expander(name):
                st.write(desc)
                st.progress(0.75)
                st.caption("Demo completion: 75%")
                st.button(f"Open {name}", key=name)

    with tabs[2]:
        st.subheader("🤖 AI Formulation Simulator")
        st.write("Adjust formulation parameters, then ask the prototype AI to predict key sensory parameters.")
        col1, col2 = st.columns(2)
        with col1:
            okara = st.slider("Okara (%)", 20, 70, 45)
            binder = st.slider("Binder (%)", 5, 30, 15)
            flour = st.slider("Flour (%)", 5, 35, 20)
        with col2:
            water = st.slider("Water (%)", 5, 30, 12)
            oil = st.slider("Oil (%)", 1, 15, 8)
            seasoning = st.slider("Seasoning (%)", 1, 10, 5)

        if st.button("🔮 Predict Formulation", type="primary"):
            st.session_state.prediction = predict(okara,binder,flour,water,oil,seasoning)

        if st.session_state.prediction:
            moisture, texture, aroma, acceptability = st.session_state.prediction
            st.divider()
            st.subheader("AI Prediction")
            a,b,c,d = st.columns(4)
            a.metric("Moisture", f"{moisture:.1f}%")
            b.metric("Texture", f"{texture:.1f}/9")
            c.metric("Aroma", f"{aroma:.1f}/9")
            d.metric("Acceptability", f"{acceptability:.1f}/9")
            st.success("Recommended for physical validation")
            st.subheader("AI Co-Pilot Explanation")
            st.write(
                "The current formulation is predicted to provide a balanced texture and sensory profile. "
                "Students should treat this prediction as decision support and validate it through the physical laboratory."
            )
            st.warning("Prototype note: prediction values currently use demo logic. Replace with a validated trained model when experimental data are available.")

    with tabs[3]:
        st.subheader("🧪 9-Point Hedonic Sensory Validation")
        st.write("After physical preparation, enter the observed sensory ratings.")
        cols = st.columns(5)
        attrs = ["Colour","Aroma","Texture","Taste","Overall Acceptability"]
        ratings = {}
        for col, attr in zip(cols, attrs):
            ratings[attr] = col.selectbox(attr, list(range(1,10)), index=6, key=attr)
        if st.button("Submit Lab Result", type="primary"):
            st.session_state.sensory = ratings
        if st.session_state.sensory:
            st.success("Lab result recorded.")
            st.dataframe(pd.DataFrame([st.session_state.sensory]), use_container_width=True)
            if st.session_state.prediction:
                actual = st.session_state.sensory["Overall Acceptability"]
                predicted = st.session_state.prediction[3]
                st.metric("Prediction vs Actual", f"{predicted:.1f} → {actual}/9", f"Error {abs(predicted-actual):.1f}")

else:
    tabs = st.tabs(["📊 Dashboard", "👩‍🎓 Student Monitoring", "🧪 Prediction vs Actual"])
    with tabs[0]:
        st.subheader("Lecturer Dashboard")
        a,b,c,d = st.columns(4)
        a.metric("Students", "32")
        b.metric("Module Completion", "86%")
        c.metric("AI Attempts", "118")
        d.metric("Intervention Alerts", "6")
        st.divider()
        df = pd.DataFrame({
            "Module":["Introduction","Halal Food","Food Sustainability","Food Innovation","Soydget Formulation"],
            "Average Score":[92,84,78,87,71]
        })
        st.bar_chart(df.set_index("Module"))
        st.subheader("Students Requiring Intervention")
        alerts = pd.DataFrame({
            "Student":["S014","S021","S027"],
            "Issue":["Formulation calculation","Halal CCP","Moisture formulation"],
            "Status":["Review","Review","Review"]
        })
        st.dataframe(alerts, use_container_width=True)

    with tabs[1]:
        st.subheader("Student Performance")
        students = pd.DataFrame({
            "Student":["S001","S002","S003","S014","S021"],
            "Modules Completed":[5,5,4,3,4],
            "Average Score":[91,88,82,61,68],
            "AI Attempts":[4,3,5,2,3],
            "Intervention":["No","No","No","Yes","Yes"]
        })
        st.dataframe(students, use_container_width=True)

    with tabs[2]:
        st.subheader("AI Prediction vs Physical Lab Validation")
        compare = pd.DataFrame({
            "Student":["S001","S002","S003","S004","S005"],
            "AI Texture":[7.4,6.8,8.1,7.2,6.9],
            "Actual Texture":[7.2,7.0,7.5,7.4,6.7],
            "Absolute Error":[0.2,0.2,0.6,0.2,0.2]
        })
        st.dataframe(compare, use_container_width=True)
        st.line_chart(compare.set_index("Student")[["AI Texture","Actual Texture"]])

st.divider()
st.caption("SOYDGET AI • NALI 2026 Prototype • Human-AI Collaborative Learning")
