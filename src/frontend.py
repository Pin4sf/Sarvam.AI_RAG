import streamlit as st
import requests
import streamlit.components.v1 as components
import base64

# Define the API endpoint
API_ENDPOINT = "http://localhost:8000"  # Update this if your FastAPI server is running on a different address

st.set_page_config(layout="wide")

st.title("NCERT Sound Chapter Interactive Learning Tools")

# Custom CSS to improve layout
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")

# Q&A section in sidebar
st.sidebar.header("Q&A")
query = st.sidebar.text_input("Ask a question about the Sound chapter:")

if st.sidebar.button("Get answer"):
    if query:
        with st.spinner("Generating response..."):
            response = requests.post(f"{API_ENDPOINT}/generate", json={"text": query})
            if response.status_code == 200:
                answer = response.json()['result']
                st.sidebar.write(answer)
                
                # Add text-to-speech button for the answer
                if st.sidebar.button("Listen to Answer"):
                    with st.spinner("Converting text to speech..."):
                        tts_response = requests.post(f"{API_ENDPOINT}/text_to_speech", json={"text": answer})
                        if tts_response.status_code == 200:
                            audio_data = tts_response.content
                            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                            audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
                            st.sidebar.markdown(audio_tag, unsafe_allow_html=True)
                        else:
                            st.sidebar.error("Failed to convert text to speech.")
            else:
                st.sidebar.error("Failed to get response from the server.")

# Text-to-Speech section in sidebar
st.sidebar.header("Text-to-Speech")
tts_text = st.sidebar.text_area("Enter text to convert to speech:")
if st.sidebar.button("Convert to Speech"):
    if tts_text:
        with st.spinner("Converting text to speech..."):
            tts_response = requests.post(f"{API_ENDPOINT}/text_to_speech", json={"text": tts_text})
            if tts_response.status_code == 200:
                audio_data = tts_response.content
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
                st.sidebar.markdown(audio_tag, unsafe_allow_html=True)
            else:
                st.sidebar.error("Failed to convert text to speech.")

# Other tools in main content area
tool = st.selectbox("Choose a tool", ["Chapter Summary", "Quiz", "Summary Flowchart", "Exam Guide"])

if tool == "Chapter Summary":
    st.header("Chapter Summary")
    if st.button("Generate Summary"):
        with st.spinner("Generating chapter summary..."):
            response = requests.get(f"{API_ENDPOINT}/chapter_summary")
            if response.status_code == 200:
                summary = response.json()['summary']
                st.markdown(summary)
            else:
                st.error("Failed to generate chapter summary.")

elif tool == "Quiz":
    st.header("Rapid Fire Quiz")
    
    # Initialize session state for quiz
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.evaluations = {}

    if not st.session_state.quiz_started:
        num_questions = st.slider("Number of questions", min_value=1, max_value=5, value=3)
        if st.button("Start Quiz"):
            with st.spinner("Generating quiz questions..."):
                response = requests.post(f"{API_ENDPOINT}/quiz", json={"num_questions": num_questions})
                if response.status_code == 200:
                    st.session_state.questions = response.json()['questions']
                    st.session_state.quiz_started = True
                    st.session_state.current_question = 0
                    st.rerun()
                else:
                    st.error("Failed to generate quiz questions.")
    else:
        # Display current question
        question = st.session_state.questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}")
        st.write(question)

        # Input for answer
        user_answer = st.text_input("Your answer:", key=f"answer_{st.session_state.current_question}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer"):
                st.session_state.answers[st.session_state.current_question] = user_answer
                eval_response = requests.post(f"{API_ENDPOINT}/evaluate_answer", 
                                              json={"question": question, "answer": user_answer})
                if eval_response.status_code == 200:
                    evaluation = eval_response.json()['evaluation']
                    st.session_state.evaluations[st.session_state.current_question] = evaluation
                    st.rerun()
                else:
                    st.error("Failed to evaluate the answer.")

        with col2:
            if st.button("Next Question"):
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.warning("This is the last question.")

        # Display evaluation if available
        if st.session_state.current_question in st.session_state.evaluations:
            st.write(st.session_state.evaluations[st.session_state.current_question])

        # Quiz progress
        st.progress((st.session_state.current_question + 1) / len(st.session_state.questions))

        # Option to end quiz
        if st.button("End Quiz"):
            st.session_state.quiz_started = False
            st.rerun()

elif tool == "Summary Flowchart":
    st.header("Chapter Summary Flowchart")
    if st.button("Generate Summary Flowchart"):
        with st.spinner("Generating chapter summary flowchart..."):
            try:
                response = requests.get(f"{API_ENDPOINT}/summary_flowchart")
                response.raise_for_status()  # Raise an exception for bad status codes
                flowchart = response.json()['flowchart']
                
                # Display the ASCII flowchart
                st.text("Chapter Summary Flowchart:")
                st.code(flowchart, language="text")
                
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to generate flowchart. Error: {str(e)}")
                if hasattr(e.response, 'status_code') and e.response.status_code == 500:
                    st.error(f"Server error details: {e.response.json().get('detail', 'No details available')}")

elif tool == "Exam Guide":
    st.header("Exam Guide")
    num_questions = st.slider("Number of questions", min_value=1, max_value=5, value=2)
    
    if st.button("Generate Exam Guide"):
        with st.spinner("Generating exam guide..."):
            response = requests.post(f"{API_ENDPOINT}/create_exam_guide", json={"num_questions": num_questions})
            if response.status_code == 200:
                exam_guide = response.json()['exam_guide']
                st.markdown(exam_guide)
            else:
                st.error("Failed to generate exam guide.")

# Add a footer
st.sidebar.markdown("---")
st.sidebar.info("Created with ❤️ by [Shivansh Fulper](#)")