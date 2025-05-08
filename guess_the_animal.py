import streamlit as st
from openai import OpenAI
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="AI Guesses Your Animal!", page_icon="🧠")

# Header image (optional)
header_path = os.path.join("assets", "header.png")
if os.path.exists(header_path):
    st.image(Image.open(header_path), use_column_width=True)

st.title("🐾 Think of an Animal... The AI Will Try to Guess It!")

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "final_guess" not in st.session_state:
    st.session_state.final_guess = None
if "round" not in st.session_state:
    st.session_state.round = 0

# Start game
if not st.session_state.game_started:
    if st.button("I'm Thinking of an Animal"):
        st.session_state.ai_messages = [
            {"role": "system", "content": "You are playing 20 Questions to guess an animal the user is thinking of. Ask smart yes/no questions to narrow it down. After each answer, ask another question. Make your final guess only when you're confident."}
        ]
        st.session_state.game_started = True
        st.session_state.round = 1
        st.session_state.final_guess = None

# Game loop
if st.session_state.game_started:

    # If last input was the user's answer, ask next question
    if st.session_state.round == 1 or (len(st.session_state.ai_messages) and st.session_state.ai_messages[-1]["role"] == "user"):

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.ai_messages
            )
            ai_reply = response.choices[0].message.content.strip()

            # Add AI's question
            st.session_state.ai_messages.append({"role": "assistant", "content": ai_reply})
            st.markdown(f"🤖 **AI asks:** {ai_reply}")

        except Exception as e:
            st.error(f"OpenAI error: {e}")

    # User input: yes/no to AI's last question
    answer = st.radio("Your answer:", ["Yes", "No"], key=f"answer_{st.session_state.round}")
    if st.button("Submit Answer", key=f"submit_{st.session_state.round}"):
        st.session_state.ai_messages.append({"role": "user", "content": answer})
        st.session_state.round += 1

    # Optional: Let AI guess after 5 rounds
    if st.session_state.round > 5 and st.button("Let the AI Guess!"):
        st.session_state.ai_messages.append({"role": "user", "content": "Make your best guess now. What animal am I thinking of?"})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.ai_messages
            )
            guess = response.choices[0].message.content.strip()
            st.session_state.final_guess = guess
            st.success(f"🤖 The AI guesses: **{guess}**")

        except Exception as e:
            st.error(f"Error getting final guess: {e}")

# Reset game
if st.button("Start Over"):
    st.session_state.ai_messages = []
    st.session_state.game_started = False
    st.session_state.final_guess = None
    st.session_state.round = 0
