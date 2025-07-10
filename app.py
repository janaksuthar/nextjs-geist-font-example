import streamlit as st
from streamlit.components.v1 import html

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUizh9UXQIBD3ZAWf-6XXYN-VGgePf88dAw0PY7ykQ0ADMag/viewform?usp=dialog"

st.set_page_config(page_title="Quiz Wrapper", layout="wide")

# Initialize session state variables
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "roll_number" not in st.session_state:
    st.session_state.roll_number = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "tab_change_count" not in st.session_state:
    st.session_state.tab_change_count = 0

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

if not st.session_state.quiz_started:
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
                st.session_state.student_name = st.session_state.name_input
                st.session_state.roll_number = st.session_state.roll_input
                st.session_state.quiz_started = True
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
    
    # Button to simulate tab change for demo
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Simulate Tab Change (Demo)", use_container_width=True):
            st.session_state.tab_change_count += 1
            st.rerun()
    
    # Reset button
    if st.button("🔄 Reset Quiz", use_container_width=True):
        st.session_state.quiz_started = False
        st.session_state.tab_change_count = 0
        st.session_state.student_name = ""
        st.session_state.roll_number = ""
        st.rerun()
