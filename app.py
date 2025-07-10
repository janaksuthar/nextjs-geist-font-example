import streamlit as st
from streamlit.components.v1 import html

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeUizh9UXQIBD3ZAWf-6XXYN-VGgePf88dAw0PY7ykQ0ADMag/viewform?usp=dialog"

st.set_page_config(page_title="Quiz Wrapper", layout="wide")

# Use session state to track if quiz is auto-submitted
if "auto_submitted" not in st.session_state:
    st.session_state.auto_submitted = False

if st.session_state.auto_submitted:
    # Show auto-submitted message
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #000000;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 1rem;
        }
        .message-box {
            max-width: 600px;
            border: 2px solid #fff;
            padding: 2rem;
            border-radius: 0.5rem;
            background-color: #111111;
            text-align: center;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        p {
            font-size: 1.25rem;
        }
        </style>
        <div class="message-box">
            <h1>Quiz Auto-Submitted</h1>
            <p>Your quiz has been automatically submitted due to tab change or loss of focus. You cannot continue the quiz.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Embed Google Form with JS to detect tab change and notify Streamlit
    component_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Quiz Wrapper</title>
      <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet" />
      <script src="https://cdn.tailwindcss.com"></script>
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
          min-height: 100vh;
        }}
      </style>
    </head>
    <body>
      <iframe id="googleForm" src="{GOOGLE_FORM_URL}" allowfullscreen></iframe>

      <script>
        function notifyStreamlit() {{
          // Send message to Streamlit to update session state
          window.parent.postMessage({{type: 'tabChangeDetected'}}, '*');
        }}

        document.addEventListener("visibilitychange", () => {{
          if (document.hidden) {{
            notifyStreamlit();
          }}
        }});

        window.addEventListener("blur", () => {{
          notifyStreamlit();
        }});
      </script>
    </body>
    </html>
    """

    # Define a Streamlit component with postMessage listener
    html(
        component_html,
        height=700,
        scrolling=True,
        # Enable communication between iframe and Streamlit
        # We will listen for postMessage in Streamlit below
    )

    # Listen for postMessage from iframe using Streamlit's experimental get_query_params hack
    # Since Streamlit does not support direct JS event listening, we use a workaround with st.experimental_get_query_params
    # Instead, we use st.experimental_rerun on message received via query param or use st.experimental_set_query_params

    # We can use st.experimental_get_query_params to detect a param like ?auto_submitted=true
    # But since we cannot set query params from JS easily, we will use a hack with st.experimental_set_query_params in a callback

    # Instead, we use st.experimental_set_query_params in a button or timer, but here we rely on the postMessage from iframe

    # So we add a listener in Streamlit to listen for postMessage from iframe
    # This is not natively supported, so we use a Streamlit component or a hack

    # For now, we will use st.experimental_rerun triggered by a button for demo purposes

    # To implement the full functionality, we need a custom Streamlit component or external library

    # As a workaround, we add a button to simulate tab change detection for demo

    if st.button("Simulate Tab Change (for demo)"):
        st.session_state.auto_submitted = True
        st.experimental_rerun()
