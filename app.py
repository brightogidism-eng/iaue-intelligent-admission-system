import streamlit as st
import pandas as pd

st.set_page_config(page_title="IAUE Intelligent Admission System", layout="wide")

# --- DATA ---
if "applicants" not in st.session_state:
    st.session_state.applicants = []

CUTOFFS = {
    "Computer Science": 180,
    "Education": 160,
    "Law": 220,
    "Nursing": 200,
    "Accounting": 180,
    "Mass Communication": 180
}

def calculate_status(jamb, post_utme, course, english, maths):
    # OLevel Check
    if english < 5 or maths < 5:
        return 0, "Not Admitted - OLevel Failed (English & Maths must be Credit)", 0
    aggregate = round((jamb / 8) + (post_utme / 2), 2)
    cutoff = CUTOFFS.get(course, 170)
    if aggregate >= cutoff:
        status = "Admitted"
    elif aggregate >= cutoff - 10:
        status = "Waiting List"
    else:
        status = "Not Admitted"
    return aggregate, status, cutoff

# --- HEADER ---
st.title("IAUE Intelligent Admission System")
st.subheader("Ignatius Ajuru University of Education - 2026/2027 Admission")
st.markdown("---")

role = st.radio("Who are you?", ["I am an APPLICANT", "I am an ADMIN"], horizontal=True)

# ================= APPLICANT =================
if role == "I am an APPLICANT":
    st.header("Applicant Application Form")

    with st.form("apply_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            jamb_reg = st.text_input("JAMB Reg Number")
            jamb = st.number_input("JAMB Score (0-400)", 0, 400, 200)
            post_utme = st.number_input("Post-UTME Score (0-100)", 0, 100, 50)
        with col2:
            course = st.selectbox("Course Applied For", list(CUTOFFS.keys()))
            english = st.selectbox("English Grade (1=A1, 5=C6, 6=D7)", [1,2,3,4,5,6,7,8,9], index=4)
            maths = st.selectbox("Maths Grade (1=A1, 5=C6, 6=D7)", [1,2,3,4,5,6,7,8,9], index=4)
            email = st.text_input("Email")

        st.markdown("### Payment - Screening Fee: N2,000")
        paid = st.checkbox("I have paid N2,000 screening fee")

        submitted = st.form_submit_button("Submit Application")

    if submitted:
        if not name or not jamb_reg:
            st.error("Please enter Name and JAMB Reg Number")
        elif not paid:
            st.error("Please confirm payment of N2,000 to proceed")
        else:
            agg, status, cutoff = calculate_status(jamb, post_utme, course, english, maths)
            new_app = {
                "Name": name,
                "JAMB Reg": jamb_reg,
                "Course": course,
                "JAMB": jamb,
                "Post-UTME": post_utme,
                "Aggregate": agg,
                "Cut-off": cutoff,
                "OLevel Credits": f"Eng:{english} Maths:{maths}",
                "Status": status,
                "Email": email
            }
            st.session_state.applicants.append(new_app)
            st.success(f"Application Submitted! Status: {status}")
            st.info(f"Aggregate: {agg} | Cut-off for {course}: {cutoff}")
            if "Waiting" in status:
                st.warning("You are on Waiting List. You may be moved to Admitted if space opens.")
            if "OLevel" in status:
                st.error("Failed because English or Maths is below Credit (C6).")

    if st.session_state.applicants:
        st.markdown("---")
        st.subheader("My Applications")
        for a in st.session_state.applicants:
            credits = a.get("OLevel Credits", "")
            st.write(f"**{a['Name']}** - {a['Course']} - Aggregate: {a['Aggregate']} | Cut-off: {a['Cut-off']} | OLevel: {credits} | Status: {a['Status']}")

# ================= ADMIN =================
else:
    st.header("Admin Dashboard")
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "admin123":
        st.success("Welcome Admin")

        apps = st.session_state.applicants
        if not apps:
            st.info("No applicants yet. Ask
