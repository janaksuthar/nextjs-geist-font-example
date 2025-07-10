import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from datetime import datetime
import io

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUizh9UXQIBD3ZAWf-6XXYN-VGgePf88dAw0PY7ykQ0ADMag/viewform?usp=dialog"

st.set_page_config(page_title="Quiz Monitoring System", layout="wide")

# Initialize session state variables
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "roll_number" not in st.session_state:
    st.session_state.roll_number = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "tab_change_count" not in st.session_state:
    st.session_state.tab_change_count = 0
if "is_instructor" not in st.session_state:
    st.session_state.is_instructor = False
if "student_records" not in st.session_state:
    st.session_state.student_records = []
if "current_session_saved" not in st.session_state:
    st.session_state.current_session_saved = False

def save_student_record():
    """Save current student session to records"""
    if not st.session_state.current_session_saved and st.session_state.quiz_started:
        record = {
            "Student Name": st.session_state.student_name,
            "Roll Number": st.session_state.roll_number,
            "Tab Changes": st.session_state.tab_change_count,
            "Quiz Start Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Completed" if st.session_state.tab_change_count == 0 else f"Warning: {st.session_state.tab_change_count} tab changes"
        }
        st.session_state.student_records.append(record)
        st.session_state.current_session_saved = True

def instructor_login():
    """Instructor login page"""
    st.markdown("""
    <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; border: 2px solid #ffffff; border-radius: 0.5rem; background-color: #111111; text-align: center;">
        <h1>Instructor Login</h1>
        <p>Enter credentials to access student records</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("instructor_login"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            if username == "jnk" and password == "123":
                st.session_state.is_instructor = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")

def instructor_dashboard():
    """Instructor dashboard to view and download records"""
    st.title("📊 Instructor Dashboard")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Student Quiz Monitoring Records")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.is_instructor = False
            st.rerun()
    
    if st.session_state.student_records:
        # Display records in a table
        df = pd.DataFrame(st.session_state.student_records)
        st.dataframe(df, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(df))
        with col2:
            st.metric("Students with Tab Changes", len(df[df["Tab Changes"] > 0]))
        with col3:
            st.metric("Average Tab Changes", f"{df['Tab Changes'].mean():.1f}")
        with col4:
            st.metric("Max Tab Changes", df["Tab Changes"].max())
        
        # Download Excel file
        st.subheader("📥 Download Records")
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Student Records', index=False)
            
            # Add summary sheet
            summary_data = {
                "Metric": ["Total Students", "Students with Tab Changes", "Students without Tab Changes", "Average Tab Changes", "Maximum Tab Changes"],
                "Value": [
                    len(df),
                    len(df[df["Tab Changes"] > 0]),
                    len(df[df["Tab Changes"] == 0]),
                    f"{df['Tab Changes'].mean():.2f}",
                    df["Tab Changes"].max()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📊 Download Excel Report",
            data=excel_data,
            file_name=f"quiz_monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        # Clear all records button
        if st.button("🗑️ Clear All Records", type="secondary"):
            st.session_state.student_records = []
            st.success("All records cleared!")
            st.rerun()
            
    else:
        st.info("No student records available yet.")
        st.markdown("Students will appear here once they start taking the quiz.")

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.main {
    background-color: #000000;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

.student-form {
    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    border: 2px solid #ffffff;
    border-radius: 0.5rem;
    background-color: #111111;
    text-align: center;
}

.warning-box {
    background-color: #ff4444;
    color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
    text-align: center;
    font-weight: 600;
}

.info-box {
    background-color: #333333;
    color: #ffffff;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Main app logic
if st.session_state.is_instructor:
    instructor_dashboard()
else:
    # Check if user wants to login as instructor
    if st.sidebar.button("👨‍🏫 Instructor Login"):
        instructor_login()
    elif not st.session_state.quiz_started:
        # Show student information form
        st.markdown("""
        <div class="student-form">
            <h1>Quiz Registration</h1>
            <p>Please enter your details before starting the quiz</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("student_info"):
            st.text_input("Student Name", key="name_input", placeholder="Enter your full name")
            st.text_input("Roll Number", key="roll_input", placeholder="Enter your roll number")
            
            submitted = st.form_submit_button("Start Quiz", use_container_width=True)
            
            if submitted:
                if st.session_state.name_input and st.session_state.roll_input:
                    # Check if student already exists
                    existing_student = any(
                        record["Roll Number"] == st.session_state.roll_input 
                        for record in st.session_state.student_records
                    )
                    
                    if existing_student:
                        st.error("This roll number has already taken the quiz!")
                    else:
                        st.session_state.student_name = st.session_state.name_input
                        st.session_state.roll_number = st.session_state.roll_input
                        st.session_state.quiz_started = True
                        st.session_state.current_session_saved = False
                        st.rerun()
                else:
                    st.error("Please fill in both name and roll number")

    else:
        # Show student info and tab change count
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <strong>Student:</strong> {st.session_state.student_name}<br>
                <strong>Roll No:</strong> {st.session_state.roll_number}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.session_state.tab_change_count > 0:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ Tab Changes: {st.session_state.tab_change_count}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-box">
                    Tab Changes: {st.session_state.tab_change_count}
                </div>
                """, unsafe_allow_html=True)
        
        # Show warning if tab changes detected
        if st.session_state.tab_change_count > 0:
            st.warning(f"⚠️ Warning: You have switched tabs {st.session_state.tab_change_count} time(s). Please stay focused on the quiz!")
        
        # Embed Google Form with JS to detect tab changes
        component_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>Quiz</title>
          <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet" />
          <style>
            body {{
              font-family: 'Inter', sans-serif;
              background-color: #000;
              color: #fff;
              margin: 0;
              padding: 0;
              height: 100vh;
              display: flex;
              flex-direction: column;
            }}
            iframe {{
              flex-grow: 1;
              border: none;
              width: 100%;
              min-height: 600px;
            }}
            .tab-counter {{
              position: fixed;
              top: 10px;
              right: 10px;
              background-color: #ff4444;
              color: white;
              padding: 10px;
              border-radius: 5px;
              font-weight: bold;
              z-index: 1000;
              display: none;
            }}
          </style>
        </head>
        <body>
          <div id="tabCounter" class="tab-counter">Tab Changes: 0</div>
          <iframe id="googleForm" src="{GOOGLE_FORM_URL}" allowfullscreen></iframe>

          <script>
            let tabChangeCount = {st.session_state.tab_change_count};
            
            function updateTabCounter() {{
              tabChangeCount++;
              const counter = document.getElementById('tabCounter');
              counter.textContent = `Tab Changes: ${{tabChangeCount}}`;
              counter.style.display = 'block';
              
              // Send message to parent window (Streamlit)
              window.parent.postMessage({{
                type: 'tabChangeDetected',
                count: tabChangeCount
              }}, '*');
            }}

            document.addEventListener("visibilitychange", () => {{
              if (document.hidden) {{
                updateTabCounter();
              }}
            }});

            window.addEventListener("blur", () => {{
              updateTabCounter();
            }});
            
            // Show current count if > 0
            if (tabChangeCount > 0) {{
              const counter = document.getElementById('tabCounter');
              counter.textContent = `Tab Changes: ${{tabChangeCount}}`;
              counter.style.display = 'block';
            }}
          </script>
        </body>
        </html>
        """

        # Embed the component
        html(component_html, height=650, scrolling=True)
        
        # Auto-save student record when quiz is completed
        save_student_record()
        
        # Button to simulate tab change for demo
        col1, col2, col3 = st.columns([1, 1, 1])
        # with col2:
        #     if st.button("🔄 Simulate Tab Change (Demo)", use_container_width=True):
        #         st.session_state.tab_change_count += 1
        #         st.rerun()
        
        # Finish quiz button (saves record)
        if st.button("✅ Finish Quiz", use_container_width=True, type="primary"):
            save_student_record()
            st.success("Quiz completed! Your responses have been recorded.")
            st.balloons()
            # Reset for next student
            st.session_state.quiz_started = False
            st.session_state.tab_change_count = 0
            st.session_state.student_name = ""
            st.session_state.roll_number = ""
            st.session_state.current_session_saved = False
            st.rerun()
