import streamlit as st
import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_data
def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
        "mcqs": [
            {
                "mcq": "multiple choice question1",
                "options": {
                    "a": "choice here1",
                    "b": "choice here2",
                    "c": "choice here3",
                    "d": "choice here4",
                },
                "correct": "correct choice option",
            },
            {
                "mcq": "multiple choice question",
                "options": {
                    "a": "choice here",
                    "b": "choice here",
                    "c": "choice here",
                    "d": "choice here",
                },
                "correct": "correct choice option",
            },
            {
                "mcq": "multiple choice question",
                "options": {
                    "a": "choice here",
                    "b": "choice here",
                    "c": "choice here",
                    "d": "choice here",
                },
                "correct": "correct choice option",
            }
        ]
    }

    PROMPT_TEMPLATE = """
    Text: {text_content}
    You are an expert in generating MCQ type quiz on the basis of provided content.
    Given the above text, create a quiz of 3 multiple choice questions keeping difficulty level as {quiz_level}.
    Make sure the questions are not repeated and check all the questions to be conforming the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide.
    Ensure to make an array of 3 MCQs referring the following response json.
    Here is the RESPONSE_JSON:

    {RESPONSE_JSON}
    """

    formatted_template = PROMPT_TEMPLATE.format(text_content=text_content, quiz_level=quiz_level, RESPONSE_JSON=json.dumps(RESPONSE_JSON))

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the correct model name
        messages=[
            {"role": "system", "content": "You are an expert in generating multiple choice questions."},
            {"role": "user", "content": formatted_template}
        ],
        temperature=0.3,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )    

    # Extract response
    extracted_response = response.choices[0].message['content'].strip()
    
    return json.loads(extracted_response).get("mcqs", [])



def main():
    st.title("RVCE QUIZ GENERATOR")

    # Input for user
    text_content = st.text_area("Paste the text contents here:")

    # Select quiz level
    quiz_level = st.selectbox("Select the level:", ["EASY", "MEDIUM", "HARD"])

    # Convert quiz level to lower casing
    quiz_level_lower = quiz_level.lower()

    # Initialize session state 
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False

    # Track if generate quiz button is clicked or not 
    if not st.session_state.quiz_generated:
        st.session_state.quiz_generated = st.button("Generate Quiz")

    if st.session_state.quiz_generated:
        # Define questions and options 
        questions = fetch_questions(text_content=text_content, quiz_level=quiz_level_lower)

        # Display questions
        selected_options = []
        correct_answers = []
        for question in questions:
            options = list(question["options"].values())
            selected_option = st.radio(question["mcq"], options)
            selected_options.append(selected_option)
            correct_answers.append(question["options"][question["correct"]])

        # Submit button
        if st.button("SUBMIT"):
            # Display selected options
            marks = 0
            st.header("RESULT: ")
            for i, question in enumerate(questions):
                selected_option = selected_options[i]
                correct_option = correct_answers[i]
                st.subheader(f"{question['mcq']}")
                st.write(f"You selected: {selected_option}")
                st.write(f"Correct answer: {correct_option}")
                if selected_option == correct_option:
                    marks += 1
            st.subheader(f"YOU SCORED {marks} OUT OF {len(questions)}")

if __name__ == "__main__":
    main()
