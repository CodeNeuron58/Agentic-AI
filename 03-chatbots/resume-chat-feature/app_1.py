import streamlit as st
import uuid
from graphy import chatbot
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="LangGraph Chat", layout="wide")
st.title("LangGraph Chatbot")

# -------------------------------
# SESSION STATE INIT
# -------------------------------

if "chat_ids" not in st.session_state:
    st.session_state.chat_ids = []

if "active_chat_id" not in st.session_state:
    # create first chat automatically
    new_id = str(uuid.uuid4())
    st.session_state.chat_ids.append(new_id)
    st.session_state.active_chat_id = new_id

# -------------------------------
# SIDEBAR (CHAT LIST)
# -------------------------------

with st.sidebar:
    st.header("Chats")

    # New chat button
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chat_ids.append(new_id)
        st.session_state.active_chat_id = new_id
        st.rerun()

    # Existing chats
    for cid in st.session_state.chat_ids:
        if st.button(cid[:8], key=cid):
            st.session_state.active_chat_id = cid
            st.rerun()

# -------------------------------
# LOAD HISTORY FROM LANGGRAPH
# -------------------------------

thread_id = st.session_state.active_chat_id

# Ask LangGraph for current state (if any)
state = chatbot.get_state(
    config={"configurable": {"thread_id": thread_id}}
)

messages = state.values.get("messages", []) if state else []

# -------------------------------
# RENDER CHAT HISTORY
# -------------------------------

for msg in messages:
    role = "assistant" if msg.type == "ai" else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# -------------------------------
# USER INPUT
# -------------------------------

user_input = st.chat_input("Type your message...")

if user_input:
    # show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # invoke LangGraph
    chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"thread_id": thread_id}},
    )

    st.rerun()
