import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Guess My Animal", page_icon="🐾")
st.title("🐾 The AI Tries to Guess Your Animal!")

if "history" not in st.session_state:
    st.session_state.history = []
if "round" not in st.session_state:
    st.session_state.round = 1
if "final_guess" not in st.session_state:
    st.session_state.final_guess = None

if st.button("I'm Thinking of an Animal") or st.session_state.round > 1:
    if st.session_state.round == 1:
        prompt = "You are playing 20 Questions to guess the animal someone is thinking of. Ask smart yes/no questions to narrow it down."
        response = model.generate_content(prompt)
    else:
        last_response = st.session_state.history[-1]["answer"]
        full_prompt = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in st.session_state.history])
        response = model.generate_content(full_prompt + "\nAsk your next yes/no question.")

    question = response.text.strip()
    st.session_state.current_question = question
    st.markdown(f"🤖 **AI asks:** {question}")

    answer = st.radio("Your answer:", ["Yes", "No"], key=st.session_state.round)
    if st.button("Submit", key=f"submit_{st.session_state.round}"):
        st.session_state.history.append({
            "question": question,
            "answer": answer
        })
        st.session_state.round += 1

    if st.session_state.round > 5:
        if st.button("Let the AI Guess!"):
            full_history = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in st.session_state.history])
            final_prompt = full_history + "\nMake your best guess: What animal am I thinking of?"
            guess = model.generate_content(final_prompt).text.strip()
            st.session_state.final_guess = guess
            st.success(f"🤖 The AI guesses: **{guess}**")

if st.button("Reset Game"):
    st.session_state.history = []
    st.session_state.round = 1
    st.session_state.final_guess = None
