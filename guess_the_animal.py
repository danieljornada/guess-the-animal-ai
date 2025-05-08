import streamlit as st
import openai
import os
from PIL import Image
import random

# --- Set up OpenAI API key ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI playing 'Guess the Animal'. Ask yes/no questions to identify the animal the user is thinking of. After enough questions, you will try to guess the animal."},
        {"role": "user", "content": "Let's start. Ask your first question."}
    ]

# --- Add fun header image ---
st.set_page_config(page_title="Guess the Animal!", page_icon="\U0001F98A")
st.image("https://cdn.pixabay.com/photo/2016/04/01/09/30/animals-1299097_960_720.png", use_column_width=True)

st.title("Guess the Animal: Human vs. AI")
st.write("**Think of an animal. The AI will try to guess it by asking yes/no questions!**")

# --- Sidebar: How AI Works ---
with st.sidebar:
    st.header("How AI is Thinking")
    st.markdown("This game uses a type of AI called a **Large Language Model (LLM)**. It works like a really smart autocomplete system that has read millions of books, websites, and facts.")
    st.markdown("The AI asks questions based on logic and patterns it has learned to narrow down your animal.")
    st.markdown("You’re helping it learn by giving clear answers!")
    st.success("Tip: Stick to 'Yes', 'No', or 'Not sure'!")

# --- Sound effects list ---
sound_effects = [
    "https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg",
    "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    "https://actions.google.com/sounds/v1/cartoon/pop.ogg"
]

# --- Display conversation ---
for msg in st.session_state.messages[2:]:
    if msg['role'] == 'assistant':
        st.markdown(f"**AI:** {msg['content']}")
    else:
        st.markdown(f"**You:** {msg['content']}")

# --- Get user reply ---
with st.form("response_form", clear_on_submit=True):
    user_input = st.text_input("Your answer (Yes / No / Not sure):")
    submitted = st.form_submit_button("Submit")

if submitted and user_input:
    # Add user response
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
        assistant_msg = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

        # Play fun sound effect
        sound = random.choice(sound_effects)
        st.audio(sound)

    except Exception as e:
        st.error(f"Error communicating with OpenAI: {e}")

# --- Reset game ---
if st.button("Restart Game"):
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI playing 'Guess the Animal'. Ask yes/no questions to identify the animal the user is thinking of. After enough questions, you will try to guess the animal."},
        {"role": "user", "content": "Let's start. Ask your first question."}
    ]
    st.experimental_rerun()

st.markdown("---")
st.info("Only respond with 'Yes', 'No', or 'Not sure' to help the AI guess correctly!")
