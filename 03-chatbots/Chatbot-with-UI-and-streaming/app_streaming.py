import streamlit as st
from Stream_Backend import chatbot
from langchain_core.messages import HumanMessage

# Set up the Streamlit page
st.set_page_config(page_title="LangGraph Chat", page_icon="💬")
st.title("LangGraph Assistant")

# Configuration for the chatbot
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Initialize chat history in session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input from chat box
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response and stream it
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            (
                message_chunk
                for message_chunk, metadata in chatbot.stream(
                    {"messages": [HumanMessage(content=prompt)]},
                    config=CONFIG,
                    stream_mode="messages"
                )
            )
        )
    # Add assistant response to chat history.
    st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
