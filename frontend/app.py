import streamlit as st
import requests


# ---------------- Custom Styling ----------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #f8fafc, #eff6ff);
    }
    .title {
        font-size: 42px;
        font-weight: 700;
        color: #0f172a;
    }
    .subtitle {
        font-size: 18px;
        color: #475569;
        margin-bottom: 20px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 12px;
    }
    .success {
        color: #16a34a;
        font-weight: 600;
    }
    .warning {
        color: #ca8a04;
        font-weight: 600;
    }
    .danger {
        color: #dc2626;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="title">AI Internship & Career Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Track your growth. Get smarter career guidance.</div>', unsafe_allow_html=True)

# ---------------- Input Section ----------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Career Analysis Input</div>', unsafe_allow_html=True)

    user_id = st.text_input("User ID", placeholder="Enter your unique user ID")
    resume_text = st.text_area(
        "Resume / Skills Input",
        placeholder="Example: I know Python, ML, FastAPI and built a machine learning project...",
        height=200
    )

    analyze_btn = st.button("Analyze My Career Progress 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- API Call ----------------
if analyze_btn:
    if not user_id or not resume_text:
        st.warning("Please enter both User ID and Resume Text.")
    else:
        with st.spinner("Analyzing your profile..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "user_id": user_id,
                        "resume_text": resume_text
                    }
                )

                if response.status_code == 200:
                    data = response.json()

                    # ---------------- Results Section ----------------
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Extracted Skills</div>', unsafe_allow_html=True)

                        if data.get("skills"):
                            for skill in data["skills"]:
                                st.success(f"✅ {skill}")
                        else:
                            st.info("No skills detected")
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Missing Skills</div>', unsafe_allow_html=True)

                        if data.get("missing_skills"):
                            for skill in data["missing_skills"]:
                                st.warning(f"⚠️ {skill}")
                        else:
                            st.success("🎉 No missing skills!")
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Improvement Status</div>', unsafe_allow_html=True)

                        improvement = data.get("improvement", "No data")

                        if improvement == "No improvement detected":
                            st.error(improvement)
                        elif "First session" in improvement:
                            st.info(improvement)
                        else:
                            st.success(improvement)

                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Project Feedback</div>', unsafe_allow_html=True)
                        st.write(data.get("project_feedback", "No project feedback"))
                        st.markdown('</div>', unsafe_allow_html=True)

                    # ---------------- AI Advice ----------------
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">AI Career Advice</div>', unsafe_allow_html=True)
                    st.write(data.get("advice", "No advice generated"))
                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running on http://127.0.0.1:8000")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
