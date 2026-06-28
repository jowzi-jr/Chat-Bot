import streamlit as st
from google import genai

# -----------------------------------------
# Streamlit page settings
# -----------------------------------------

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🗿",
    layout="centered"
)

st.title("🗿 Chat With Mee-DAASAN")

st.write(
    "Talk to DAASAN,definetely doesnt use GOOGLE's API to respond back."
)

# -----------------------------------------
# Gemini client
# -----------------------------------------

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------------------
# Initialize chat history
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------
# Display previous chat messages
# -----------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------------------
# User input
# -----------------------------------------

user_prompt = st.chat_input("Enthaa parayan ullath")

if user_prompt:
    # Store and display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.write(user_prompt)

    # Build conversation context
    conversation = ""

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        conversation += f"{role}: {content}\n"

    prompt = f"""
    You are DAASAN (definitely not an AI). Your football GOAT is Zlatan Ibrahimovic,defend your GOAT if someone says otherwise.And you are a football fan.
    Dont state this when someone asks anything unrelated to football, talk to them normally.
    Answer clearly and simply.

    Conversation so far:
    {conversation}

    Assistant:
    """

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            assistant_reply = response.text
            st.write(assistant_reply)

    # Store assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# -----------------------------------------
# Clear chat button
# -----------------------------------------

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
