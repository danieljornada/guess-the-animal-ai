import streamlit as st
from PIL import Image
import random
import os
from openai import OpenAI

# Load OpenAI API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set up Streamlit page
st.set_page_config(page_title="Guess the Animal!", page_icon="🐾")

# Display header image (make sure this exists in /assets)
header_image_path = os.path.join("assets", "header.png")
if os.path.exists(header_image_path):
    st.image(Image.open(header_image_path), use_column_width=True)

st.title("🎮 Guess the Animal — Can You Beat the AI?")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "secret_animal" not in st.session_state:
    st.session_state.secret_animal = ""

# List of possible animals
ANIMALS = ["elephant", "giraffe", "kangaroo", "penguin", "panda", "octopus", "dolphin", "tiger", "eagle"]

# Start game
if not st.session_state.game_started:
    if st.button("Start Game"):
        st.session_state.secret_animal = random.choice(ANIMALS)
        st.session_state.messages.append({"role": "system", "content": f"You are thinking of an animal. Try to answer the user's yes/no questions to help them guess it. The secret animal is: {st.session_state.secret_animal}."})
        st.session_state.game_started = True
        st.success("Ask me yes/no questions to guess the animal!")

# Gameplay
if st.session_state.game_started:
    user_input = st.text_input("Your question (yes/no only):", key="user_input")
    if st.button("Ask"):
        if user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input.strip()})

            try:
                # Get AI's response from OpenAI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                ai_message = response.choices[0].message.content.strip()
                st.session_state.messages.append({"role": "assistant", "content": ai_message})

                st.markdown(f"**AI says:** {ai_message}")

            except Exception as e:
                st.error(f"Error communicating with OpenAI: {e}")

    # Let user guess
    guess = st.text_input("Your final guess (type the animal name):", key="guess_input")
    if st.button("Submit Guess"):
        if guess.strip().lower() == st.session_state.secret_animal:
            st.success(f"🎉 You got it! It was **{st.session_state.secret_animal}**!")
        else:
            st.error(f"❌ Nope, it was **{st.session_state.secret_animal}**.")

        st.session_state.game_started = False
        st.session_state.messages = []

# Option to reset game
if st.button("Start a New Game"):
    st.session_state.game_started = False
    st.session_state.secret_animal = ""
    st.session_state.messages = []
