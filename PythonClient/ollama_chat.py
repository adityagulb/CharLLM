import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# Initialize the ChatOllama model
chat = ChatOllama(model="gemma3:1b")

# Streamlit page config
st.set_page_config(page_title="Chat with Gemma3", page_icon="🤖", layout="wide")
st.title("Chat with Gemma3")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Chat input box
if prompt := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state["messages"].append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream model response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_text = ""

        for chunk in chat.stream(st.session_state["messages"]):
            response_text += chunk.content
            message_placeholder.markdown(response_text + "▌")

        message_placeholder.markdown(response_text)

    # Save AI response to history
    st.session_state["messages"].append(AIMessage(content=response_text))
