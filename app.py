import streamlit as st
import pandas as pd

st.set_page_config(page_title="IAUE Admission System")
st.title("IAUE Intelligent Admission System")

if "applicants" not in st.session_state:
    st.session_state.applicants = []

role = st.selectbox("Who are you?", ["I am an APPLICANT", "I am an ADMIN"])

if role == "I am an APPLICANT":
    st.header("Apply Now")
    name = st.text_input("Full Name")
    jamb_reg = st.text_input("JAMB Reg Number")
    jamb = st.number_input("JAMB Score", 0, 400, 200)
    post = st.number_input("Post-UTME Score", 0, 100, 50)
    paid = st.checkbox("I have paid")
    course = st.selectbox("Course", ["Computer Science", "Law", "Medicine", "Accounting"])
    if st.button("Submit Application"):
        agg = (jamb/8) + (post/2)
        status = "Admitted" if agg >= 55 else "Not Admitted"
        st.session_state.applicants.append({"Name": name, "JAMB Reg": jamb_reg, "JAMB": jamb, "Post-UTME": post, "Aggregate": agg, "Course": course, "Status": status, "Paid": paid})
        st.success(f"{status} - Aggregate: {agg}")
else:
    st.header("Admin Dashboard")
    pwd = st.text_input("Admin Password", type="password")
    login = st.button("Login as Admin")
    if login and pwd == "admin123":
        st.success("Welcome Admin!")
        apps = st.session_state.applicants
        if not apps:
            st.info("No applicants yet.")
        else:
            st.write(f"Total Applicants: {len(apps)}")
            st.dataframe(apps)
    elif login:
        st.error("Wrong password. Try admin123")
