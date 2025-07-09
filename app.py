import streamlit as st
from openai import OpenAI
from streamlit_chat import message

st.set_page_config(page_title="English Chat Bot")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💬 Chat with an English Tutor")

# Level selector
level = st.selectbox("Choose your English level:", ["A1", "A2", "B1", "B2", "C1", "C2"])
correction_mode = st.toggle("✍️ Correct my sentence", value=False)

# System prompt with level info
if "messages" not in st.session_state:
    system_prompt = f"""You are a helpful and friendly English tutor.
Speak clearly and simply, adapted to CEFR level {level}.
If correction mode is ON, correct the user's grammar and explain the changes briefly.
Otherwise, answer normally and provide examples."""
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
else:
    # Update system prompt if level changed
    st.session_state.messages[0]["content"] = f"""You are a helpful and friendly English tutor.
Speak clearly and simply, adapted to CEFR level {level}.
If correction mode is ON, correct the user's grammar and explain the changes briefly.
Otherwise, answer normally and provide examples."""

# Display chat messages
for i, msg in enumerate(st.session_state.messages[1:]):  # Skip system message
    message(msg["content"], is_user=(msg["role"] == "user"), key=str(i))

# Chat input
prompt = st.chat_input("Type something in English...")

if prompt:
    user_prompt = f"[Correction mode: {'ON' if correction_mode else 'OFF'}]\n{prompt}"
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    message(reply, is_user=False, key=str(len(st.session_state.messages)))
