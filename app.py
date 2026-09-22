import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from memory_agent import graph   # imports the compiled graph from memory_agent.py

load_dotenv(r"C:\Users\DELL\langchain-academy\module-5\studio\.env.example", override=True)

def get_text(content):
    """Extract plain reply text, whether content is a string or a list of blocks (Gemini)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            else:
                parts.append(str(block))
        return "".join(parts)
    return str(content)

st.title("Memory Agent Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    config = {"configurable": {"thread_id": "1", "user_id": "Lance"}}
    result = graph.invoke({"messages": [HumanMessage(content=prompt)]}, config)
    reply = get_text(result["messages"][-1].content)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)