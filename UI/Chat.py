import time

import streamlit as st
from LLM.Conversation import Conversation

st.title('💬 AI Assistant Unisc - PPGSPI')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chatbot = Conversation()
    st.session_state.chain_qa = st.session_state.chatbot.create_load_qa()

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if question := st.chat_input("Pergunte qualquer coisa"):
    st.session_state.messages.append({'role': 'user', 'content': question})

    with st.chat_message('user'):
        st.markdown(question)

    result = st.session_state.chatbot.process_run_qa(question, st.session_state.chain_qa)

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = result

        for chunk in assistant_response.split():
            full_response += chunk + ' '
            time.sleep(0.05)

            message_placeholder.markdown(full_response + '▌')
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
