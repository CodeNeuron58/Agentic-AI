import streamlit as st
from Backend import chatbot

st.set_page_config(page_title="LangGraph Chat", page_icon="💬")
st.title("LangGraph Assistant")

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is on your mind?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Prepare input for chatbot
        initial_input = {"messages": [("user", prompt)]}
        response = chatbot.invoke(initial_input, config=CONFIG)
        output_text = response["messages"][-1].text
        st.markdown(output_text)
        st.session_state.chat_history.append({"role": "assistant", "content": output_text})
