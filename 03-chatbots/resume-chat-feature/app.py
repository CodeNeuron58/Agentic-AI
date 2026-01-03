import streamlit as st
from resume_chat import chatbot
from langchain_core.messages import HumanMessage
import uuid

# Utility functions
# Function to generate a unique ID
def generate_unique_id():
    return str(uuid.uuid4())

# Function to reset the chat
def reset_chat():
    st.session_state.session_id = generate_unique_id()
    add_chat_session(st.session_state.session_id)
    st.session_state.chat_history = []
    
def add_chat_session(session_id):
    if session_id not in st.session_state.chat_sessions:
        st.session_state.chat_sessions.append(session_id)
        
def load_conversation(session_id):
    return chatbot.get_state(config={'configurable': {'thread_id': session_id}}).values["messages"]
    
# Set up the Streamlit page
st.set_page_config(page_title="LangGraph Chat", page_icon="💬")
st.title("LangGraph Assistant")

# Initialize chat history in session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# Initialize session ID if not present
if "session_id" not in st.session_state:
    st.session_state.session_id = generate_unique_id()
    
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
    
add_chat_session(st.session_state.session_id)
    
    
    
# Sidebar UI
st.sidebar.title("LangGraph Assistant")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversation History")

for session_id in st.session_state.chat_sessions:
    if st.sidebar.button(f"Session ID: {session_id}"):
        st.session_state.session_id = session_id
        messages = load_conversation(session_id)
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})
        st.session_state.chat_history = temp_messages

# Configuration for the chatbot
CONFIG = {'configurable': {'thread_id': st.session_state.session_id}}

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
