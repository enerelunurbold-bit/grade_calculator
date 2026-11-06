import streamlit as st
import pandas as pd
import altair as alt

st.title("University Grade Calculator")
st.write("Choose your degree and enter your subject scores to view your average, estimated GPA, and score chart. Subject lists and grading information are based on MyAUM.")

subjects = {'Business Administration': ['Cost Management', 'Operations Management', 'Project Management', 'Human Resource Management', 'Leadership', 'Business Valuation', 'Quantitative Analysis', 'Strategic Management'], 'International Business': ['Cultures in Business', 'Current Issues in Trade', 'Operations Management', 'Project Management', 'Human Resource Management', 'International Economics', 'Leadership', 'Strategic Management'], 'Accounting': ['Intermediate Accounting', 'Intermediate Accounting II', 'Cost Management', 'Business Valuation', 'Corporate Finance', 'Financial Management', 'Quantitative Analysis', 'Strategic Management'], 'Marketing Management': ['Advanced Marketing', 'Digital Marketing', 'Brand Management', 'Consumer Behavior', 'Marketing Research', 'Content Marketing', 'Personal Sales', 'Strategic Management'], 'Financial Management': ['Business Valuation', 'Corporate Finance', 'Quantitative Analysis', 'Financial Management', 'Investment Management', 'Financial Markets', 'International Finance', 'Strategic Management'], 'Data Science': ['Introduction to Data Science', 'Quantitative Analysis', 'Introduction to Python', 'Intermediate Python', 'Machine Learning', 'Deep Learning', 'Capstone Project final', 'Business Intelligence', 'Strategic Management']}

degree = st.selectbox("Choose your degree", list(subjects.keys()))
st.subheader("1. Select your subjects")
selected = []
with st.container(border=True):
    columns = st.columns(2)
    for index, subject in enumerate(subjects[degree]):
        with columns[index % 2]:
            
            if st.checkbox(subject, key="select_" + degree + subject):
                selected.append(subject)

if len(selected) > 0:
    st.subheader("2. Enter your scores")
    with st.form("grades_" + degree):
        scores = []
        columns = st.columns(2)
        for index, subject in enumerate(selected):
            with columns[index % 2]:
                score = st.number_input(subject, min_value=0, max_value=100, value=None, placeholder="Enter score (0–100)", key="score_" + degree + subject)
                scores.append(score)
        submitted = st.form_submit_button("Calculate GPA", type="primary")
else:
    submitted = False
    st.info("Select the subjects you want to include.")

if submitted and None in scores:
    st.warning("Please enter a score for every selected subject.")
elif submitted:
    credits = []
    gpas = []
    grade_points = []
    statuses = []
    for subject, score in zip(selected, scores):
        credit = 3
        if subject == "Introduction to Data Science":
            credit = 1

        if score >= 93:
            gpa = 4.0
        elif score >= 60:
            gpa = score / 20 - 1
        else:
            gpa = 0.0

        if score >= 60:
            status = "Pass"
        else:
            status = "Fail / No Credit"

        credits.append(credit)
        gpas.append(gpa)
        grade_points.append(gpa * credit)
        statuses.append(status)

    st.subheader("3. Your results")
    average = sum(scores) / len(scores)
    total_credits = sum(credits)
    overall_gpa = sum(grade_points) / total_credits

    st.metric("Average score", str(round(average, 1)) + " / 100")
    st.metric("GPA for selected subjects", format(overall_gpa, ".2f") + " / 4.00")
    st.write("Credits attempted:", total_credits)
    st.caption("Average score gives each subject equal weight. GPA is weighted by credits, including failed courses.")

    data = pd.DataFrame({"Subject": selected, "Score": scores, "Credits": credits, "Course GPA": gpas, "Result": statuses})
    st.subheader("Your scores")
    st.dataframe(data.round(2), hide_index=True)
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("Subject:N", sort=None, title="Subject"),
        y=alt.Y("Score:Q", title="Score (%)", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(values=[0, 20, 40, 60, 80, 100])),
        tooltip=["Subject", "Score"]
    )
    st.altair_chart(chart, use_container_width=True)

    with st.expander("How GPA is calculated"):
        st.write("93–100: GPA = 4.0")
        st.write("60–92: GPA = score / 20 - 1")
        st.write("Below 60: Fail / No Credit, GPA = 0.0")
        st.write("Grade points = course GPA × credits")
        st.write("Overall GPA = total grade points / total credits attempted")
