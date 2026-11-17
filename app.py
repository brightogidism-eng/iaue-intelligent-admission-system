import streamlit as st
import pandas as pd
import datetime, random

st.set_page_config(page_title="IAUE Intelligent Admission System", page_icon="🎓", layout="centered")

# ===== REAL IAUE DATA =====
FACULTIES = {
    "Faculty of Natural & Applied Sciences": {"cutoff": 60, "courses": ["BSc Computer Science", "BSc Cyber Security", "BSc Biology", "BSc Chemistry", "BSc Mathematics", "BSc Physics", "BSc Information Technology"], "venue": "Faculty of Natural & Applied Sciences Hall", "day": "Monday 9:00 AM"},
    "Faculty of Administration & Management": {"cutoff": 55, "courses": ["BSc Marketing", "BSc Accounting", "BSc Management", "BSc Banking & Finance", "BSc Office & Information Management"], "venue": "Admin Block, Main Campus", "day": "Tuesday 9:00 AM"},
    "Faculty of Social Sciences": {"cutoff": 50, "courses": ["BSc Economics", "BSc Political Science", "BSc Sociology", "BSc Public Administration", "BSc Geography"], "venue": "Social Sciences Lecture Hall", "day": "Wednesday 9:00 AM"},
    "Faculty of Education": {"cutoff": 45, "courses": ["BSc.Ed Education & Biology", "BSc.Ed Education & Computer Science", "B.A.Ed Education & English", "B.Ed Primary Education", "B.Ed Early Childhood Education"], "venue": "Education Faculty Hall", "day": "Thursday 9:00 AM"},
    "Faculty of Humanities": {"cutoff": 45, "courses": ["B.A English & Communication Arts", "B.A History", "B.A Theatre Arts", "B.A Fine & Applied Arts", "B.A Music"], "venue": "Humanities Hall", "day": "Thursday 11:00 AM"},
    "Faculty of Agriculture": {"cutoff": 45, "courses": ["BSc Agriculture", "BSc Agricultural Economics", "BSc Fisheries", "BSc Forestry"], "venue": "Agric Faculty Hall", "day": "Friday 9:00 AM"},
    "Faculty of Vocational & Technical Education": {"cutoff": 45, "courses": ["BSc.Ed Agricultural Education", "BSc.Ed Technical Education", "BSc.Ed Business Education"], "venue": "Vocational Hall", "day": "Friday 11:00 AM"},
}
IAUE_JAMB_CUTOFF = 150
ADMIN_PASSWORD = "admin123"
GRADES = ["A1", "B2", "B3", "C4", "C5", "C6", "D7", "E8", "F9"]
CREDIT_GRADES = ["A1", "B2", "B3", "C4", "C5", "C6"]

# ===== SESSION =====
if "users" not in st.session_state: st.session_state.users = {}
if "applicants" not in st.session_state: st.session_state.applicants = []
if "results" not in st.session_state: st.session_state.results = {}
if "role" not in st.session_state: st.session_state.role = None
if "current_user" not in st.session_state: st.session_state.current_user = None
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "pay_ref" not in st.session_state: st.session_state.pay_ref = ""

st.title("🎓 IAUE Intelligent Admission System")
st.write("**Ignatius Ajuru University of Education, Rumuolumeni, Port Harcourt**")
st.caption("📢 Announcement: IAUE 2026/2027 Post-UTME Screening starts soon. JAMB Cut-off 150. First Choice Only. Check your Faculty venue on your slip.")
st.write("---")

if st.session_state.role:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.role = None; st.session_state.current_user = None; st.session_state.is_admin = False; st.rerun()

# ===== LANDING =====
if st.session_state.role is None:
    st.header("Welcome to IAUE Admission Portal 2026/2027")
    st.write("Select who you are:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👨‍🎓 I am an APPLICANT", use_container_width=True):
            st.session_state.role = "applicant"; st.rerun()
    with c2:
        if st.button("🔐 I am an ADMIN", use_container_width=True):
            st.session_state.role = "admin"; st.rerun()
    st.info("**Real IAUE Rules:** JAMB >=150 | First Choice | 5 O'Level Credits (English & Maths must be Credit) | Aggregate = (JAMB/8)+(Post-UTME/2) | Ranking by Faculty Quota | Waiting List if close to cut-off")

# ===== ADMIN LOGIN =====
elif st.session_state.role == "admin" and not st.session_state.is_admin:
    st.header("🔐 Admin Login")
    pwd = st.text_input("Admin Password", type="password")
    if st.button("Login as Admin"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.is_admin = True; st.rerun()
        else: st.error("Wrong password")
    st.caption("Demo: admin123")
    if st.button("⬅️ Back"):
        st.session_state.role = None; st.rerun()

# ===== ADMIN DASHBOARD - PROFESSIONAL =====
elif st.session_state.role == "admin" and st.session_state.is_admin:
    st.header("🔐 IAUE Admin Dashboard")
    if not st.session_state.applicants:
        st.write("No applicant yet.")
    else:
        df = pd.DataFrame(st.session_state.applicants)
        # Metrics
        total = len(df)
        admitted = (df["Status"] == "ADMITTED ✅").sum()
        waiting = (df["Status"] == "WAITING LIST ⏳").sum()
        not_adm = (df["Status"] == "NOT ADMITTED ❌").sum()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total", total); m2.metric("Admitted ✅", admitted); m3.metric("Waiting ⏳", waiting); m4.metric("Not Admitted ❌", not_adm)

        # FEATURE 4: SEARCH + FILTER + EXPORT
        st.subheader("🔍 Search & Filter Applicants")
        search = st.text_input("Search by Name, JAMB No, App No, Username")
        fac_filter = st.selectbox("Filter by Faculty", ["All Faculties"] + list(FACULTIES.keys()))
        status_filter = st.selectbox("Filter by Status", ["All Status", "ADMITTED ✅", "WAITING LIST ⏳", "NOT ADMITTED ❌"])
        filtered = df.copy()
        if search:
            filtered = filtered[filtered.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)]
        if fac_filter != "All Faculties":
            filtered = filtered[filtered["Faculty"] == fac_filter]
        if status_filter != "All Status":
            filtered = filtered[filtered["Status"] == status_filter]
        st.write(f"Showing {len(filtered)} applicants")
        st.dataframe(filtered)

        # Export
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Filtered List as CSV / Excel", csv, "IAUE_Applicants.csv", "text/csv")

        tab1, tab2, tab3 = st.tabs(["✅ Admitted", "⏳ Waiting List", "❌ Not Admitted"])
        with tab1: st.dataframe(df[df["Status"] == "ADMITTED ✅"])
        with tab2:
            st.dataframe(df[df["Status"] == "WAITING LIST ⏳"])
            st.caption("Admin can move Waiting List to Admitted if quota remains. Use App No below.")
            move_no = st.text_input("App No to Move from Waiting to Admitted")
            if st.button("Move to Admitted"):
                for a in st.session_state.applicants:
                    if a["App No"] == move_no and a["Status"] == "WAITING LIST ⏳":
                        a["Status"] = "ADMITTED ✅"; st.success(f"{move_no} moved to Admitted!"); st.rerun()
        with tab3: st.dataframe(df[df["Status"] == "NOT ADMITTED ❌"])
        st.write("**Admission by Faculty:**"); st.bar_chart(df["Faculty"].value_counts())

    st.write("---")
    st.subheader("Upload Result for Admitted Student")
    app_no2 = st.text_input("Application No")
    rc1 = st.number_input("GST 101", 0, 100, 70); rc2 = st.number_input("CSC 101", 0, 100, 70); rc3 = st.number_input("MTH 101", 0, 100, 70)
    if st.button("Save Result"):
        if app_no2:
            st.session_state.results[app_no2] = {"GST 101": rc1, "CSC 101": rc2, "MTH 101": rc3}; st.success("Result saved!")

# ===== APPLICANT CREATE / LOGIN =====
elif st.session_state.role == "applicant" and st.session_state.current_user is None:
    st.header("👨‍🎓 Applicant Account")
    t1, t2 = st.tabs(["📝 Create Account", "🔑 Login"])
    with t1:
        new_user = st.text_input("Choose Username", key="nu"); new_pass = st.text_input("Choose Password", type="password", key="np"); full_name = st.text_input("Full Name", key="fn")
        if st.button("Create My IAUE Account"):
            if not new_user or not new_pass or not full_name: st.error("Fill all")
            elif new_user in st.session_state.users: st.error("Username exists, login")
            else:
                st.session_state.users[new_user] = {"password": new_pass, "name": full_name}; st.success("Account created! Go to Login tab.")
    with t2:
        log_user = st.text_input("Username", key="lu"); log_pass = st.text_input("Password", type="password", key="lp")
        if st.button("Login"):
            if log_user in st.session_state.users and st.session_state.users[log_user]["password"] == log_pass:
                st.session_state.current_user = log_user; st.rerun()
            else: st.error("Wrong Username or Password")
    if st.button("⬅️ Back"):
        st.session_state.role = None; st.rerun()

# ===== APPLICANT DASHBOARD =====
elif st.session_state.role == "applicant" and st.session_state.current_user is not None:
    username = st.session_state.current_user; user_name = st.session_state.users[username]["name"]
    st.header(f"Welcome, {user_name} ({username})")
    my_apps = [a for a in st.session_state.applicants if a.get("Username") == username]
    menu = st.sidebar.selectbox("My Menu", ["📝 Apply for Admission", "🔍 Check If Admitted", "🖨️ Print Slip", "📊 View My Result"])

    if menu == "📝 Apply for Admission":
        if my_apps:
            st.warning("You have already applied. Go to Check If Admitted."); st.write(my_apps[0])
        else:
            # FEATURE 3: PAYMENT
            st.subheader("Step 1: Screening Fee Payment (₦2,000)")
            st.write("IAUE Screening Fee: **₦2,000**. Click to generate your Payment Reference.")
            if st.button("Generate Payment Reference"):
                st.session_state.pay_ref = f"IAUE-PAY-{random.randint(1000,9999)}"
            if st.session_state.pay_ref:
                st.success(f"Your Payment Reference: **{st.session_state.pay_ref}** - Copy am. (Demo: Payment assumed successful)")
            pay_input = st.text_input("Enter Payment Reference to Continue (e.g IAUE-PAY-1234)", value=st.session_state.pay_ref)

            st.subheader("Step 2: Application Form")
            with st.form("apply_form"):
                jamb_no = st.text_input("JAMB Reg Number"); phone = st.text_input("Phone"); email = st.text_input("Email")
                gender = st.selectbox("Gender", ["Male", "Female"]); state = st.text_input("State of Origin")
                choice = st.selectbox("Did you choose IAUE as First Choice?", ["Yes - First Choice", "No - Second Choice"])
                faculty = st.selectbox("Choose Faculty / School", list(FACULTIES.keys()))
                course = st.selectbox("Choose Course / Department", FACULTIES[faculty]["courses"])
                jamb_score = st.number_input("JAMB Score (0-400)", 0, 400, 220)
                post_utme = st.number_input("IAUE Post-UTME / Screening Score (0-100)", 0, 100, 60)
                # FEATURE 1: O'LEVEL CHECK
                st.write("**Step 3: O'Level Results (5 Credits Required)**")
                eng = st.selectbox("English Language Grade", GRADES)
                maths = st.selectbox("Mathematics Grade", GRADES)
                subj3 = st.text_input("Subject 3 (e.g Biology)"); grade3 = st.selectbox("Grade 3", GRADES, key="g3")
                subj4 = st.text_input("Subject 4 (e.g Chemistry)"); grade4 = st.selectbox("Grade 4", GRADES, key="g4")
                subj5 = st.text_input("Subject 5 (e.g Physics)"); grade5 = st.selectbox("Grade 5", GRADES, key="g5")
                submit = st.form_submit_button("Submit Application")
            if submit:
                if not pay_input or not pay_input.startswith("IAUE-PAY-"):
                    st.error("Invalid Payment Reference. Generate one above and enter it.")
                elif not jamb_no:
                    st.error("Enter JAMB Reg Number")
                elif choice != "Yes - First Choice":
                    st.error("IAUE requires First Choice only.")
                elif jamb_score < IAUE_JAMB_CUTOFF:
                    st.error(f"IAUE General Cut-off na {IAUE_JAMB_CUTOFF}. Your JAMB {jamb_score} too low.")
                elif eng not in CREDIT_GRADES or maths not in CREDIT_GRADES:
                    st.error(f"O'Level Failed: English ({eng}) and Maths ({maths}) must be Credit (A1-C6). IAUE requires Credit in both.")
                else:
                    all_grades = [eng, maths, grade3, grade4, grade5]
                    credits = sum(1 for g in all_grades if g in CREDIT_GRADES)
                    if credits < 5:
                        st.error(f"You have only {credits} Credits. IAUE requires 5 Credits.")
                    else:
                        aggregate = (jamb_score / 8) + (post_utme / 2)
                        cutoff = FACULTIES[faculty]["cutoff"]
                        # FEATURE 2: WAITING LIST
                        if aggregate >= cutoff:
                            status = "ADMITTED ✅"; reason = f"Aggregate {round(aggregate,2)} meets Faculty cut-off {cutoff}."
                        elif aggregate >= cutoff - 5:
                            status = "WAITING LIST ⏳"; reason = f"Aggregate {round(aggregate,2)} close to cut-off {cutoff}. You are on Waiting List. If quota remains, Admin can admit you."
                        else:
                            status = "NOT ADMITTED ❌"; reason = f"Aggregate {round(aggregate,2)} below cut-off {cutoff}."
                        app_no = f"IAUE/2026/{len(st.session_state.applicants)+1:03d}"
                        data = {"App No": app_no, "Username": username, "Name": user_name, "JAMB No": jamb_no, "Phone": phone, "Email": email, "Gender": gender, "State": state, "Faculty": faculty, "Course": course, "JAMB": jamb_score, "Post-UTME": post_utme, "Aggregate": round(aggregate,2), "Cut-off": cutoff, "Status": status, "Payment Ref": pay_input, "O'Level Credits": credits, "Screening Venue": FACULTIES[faculty]["venue"], "Screening Day": FACULTIES[faculty]["day"], "Date": str(datetime.date.today())}
                        st.session_state.applicants.append(data)
                        st.success("Application Successful!"); st.info(f"Your App No: **{app_no}** | Payment: {pay_input} | O'Level Credits: {credits}/5")
                        st.write(f"Aggregate: {round(aggregate,2)} | Cut-off: {cutoff} | **{status}**"); st.write(reason)
                        if "ADMITTED" in status: st.balloons()

    elif menu == "🔍 Check If Admitted":
        st.subheader("Check If You Are Admitted")
        if not my_apps: st.warning("You have not applied yet.")
        else:
            a = my_apps[0]
            st.write(f"**Name:** {a['Name']} | **App No:** {a['App No']} | **Payment:** {a.get('Payment Ref','')}")
            st.write(f"**Faculty:** {a['Faculty']} | **Course:** {a['Course']}")
            st.write(f"**Aggregate:** {a['Aggregate']} | Cut-off: {a['Cut-off']} | O'Level Credits: {a.get(\"O'Level Credits\",'')} ")
            st.write(f"**Screening:** {a.get('Screening Day','')} at {a.get('Screening Venue','')}")
            if a["Status"] == "ADMITTED ✅": st.success("🎉 CONGRATULATIONS! YOU ARE ADMITTED TO IAUE!")
            elif a["Status"] == "WAITING LIST ⏳": st.warning("⏳ You are on WAITING LIST. Keep checking. Admin may move you to Admitted if quota remains.")
            else: st.error("Sorry, NOT ADMITTED. Higher aggregate candidates ranked first.")

    elif menu == "🖨️ Print Slip":
        st.subheader("Print Your IAUE Slip")
        if not my_apps: st.warning("Apply first.")
        else:
            a = my_apps[0]
            slip = f"""<html><body style="font-family:Arial; padding:20px; border:3px solid #0a4d0a;">
            <h2 style="text-align:center; color:#0a4d0a;">IGNATIUS AJURU UNIVERSITY OF EDUCATION</h2>
            <p style="text-align:center;">Rumuolumeni, Port Harcourt</p><h3 style="text-align:center;">APPLICATION SLIP 2026/2027</h3><hr>
            <p><b>App No:</b> {a['App No']} | <b>Username:</b> {a['Username']} | <b>Payment Ref:</b> {a.get('Payment Ref','')}</p>
            <p><b>Name:</b> {a['Name']}</p><p><b>JAMB No:</b> {a['JAMB No']}</p>
            <p><b>Faculty:</b> {a['Faculty']}</p><p><b>Course:</b> {a['Course']}</p>
            <p><b>JAMB:</b> {a['JAMB']} | <b>Post-UTME:</b> {a['Post-UTME']} | <b>Aggregate:</b> {a['Aggregate']} | <b>Cut-off:</b> {a['Cut-off']}</p>
            <p><b>O'Level Credits:</b> {a.get("O'Level Credits",'')}/5 | <b>Status:</b> {a['Status']}</p>
            <p><b>Screening:</b> {a.get('Screening Day','')} at {a.get('Screening Venue','')}</p>
            <p><b>Date:</b> {a['Date']}</p><hr><p>Applicant Sign: __________ Admission Officer Stamp: __________</p></body></html>"""
            st.markdown(slip, unsafe_allow_html=True)
            st.download_button("⬇️ Download / Print Slip", slip, file_name=f"{a['App No']}.html", mime="text/html")

    elif menu == "📊 View My Result":
        st.subheader("My Result")
        if not my_apps: st.warning("Apply first.")
        elif my_apps[0]["Status"] != "ADMITTED ✅": st.warning("You are not admitted yet, so no result. Waiting List students also no result yet.")
        else:
            a = my_apps[0]
            res = st.session_state.results.get(a["App No"], {"GST 101": 78, "CSC 101": 85, "MTH 101": 65})
            df = pd.DataFrame(list(res.items()), columns=["Course", "Score"]); st.table(df)
            avg = sum(res.values())/len(res); st.write(f"**Average:** {round(avg,2)} | **Grade:** {'First Class' if avg>=70 else 'Second Class Upper' if avg>=60 else 'Second Class Lower' if avg>=50 else 'Third Class'}")
