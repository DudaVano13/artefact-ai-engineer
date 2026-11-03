"""Streamlit chat UI connected to a local Ollama model (no paid API)."""
import streamlit as st
from agent import Agent

st.set_page_config(page_title='Empório da Música', page_icon='🎵')
st.title('🎵 Empório da Música')
st.caption('Local AI prototype · Ollama · demonstration dataset')

if 'agent' not in st.session_state:
    st.session_state.agent = Agent()
    st.session_state.messages = []

if st.sidebar.button('Nova conversa'):
    st.session_state.agent = Agent()
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if prompt := st.chat_input('Como podemos ajudar?'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)
    try:
        with st.spinner('Consultando...'):
            reply = st.session_state.agent.reply(prompt)
    except Exception as exc:
        reply = ('Não consegui acessar o modelo local. Confira se o Ollama está instalado, '
                 'aberto e se você executou `ollama pull qwen2.5:3b`. '
                 f'Detalhes técnicos: {type(exc).__name__}: {exc}')
    st.session_state.messages.append({'role': 'assistant', 'content': reply})
    with st.chat_message('assistant'):
        st.write(reply)
