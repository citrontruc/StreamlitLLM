import streamlit as st
from helper.conversation_agent import ConversationAgent
from helper.ui_helper import UIHelper

st.sidebar.markdown("Interrogez vos données 🕵️‍♀️")
st.sidebar.markdown("Permet d'interroger les données présentes dans le dossier data.")

st.title("Interrogez vos données 🕵️‍♀️")
st.markdown("""
Ce modèle interroge les règles de base du jeu donjons et dragons, disponibles à [cette adresse](https://www.aidedd.org/adj/telechargement/).
Il possède les règles en français et répondra donc sans doute mieux aux questions en français.
        
""")

pdf_uiagent = UIHelper("🕵️‍♀️")
competency_analysis_agent = ConversationAgent()

# The messages between user and assistant are kept in the session_state (the local storage)
if "message_hist" not in st.session_state:
    st.session_state.message_hist = []

pdf_uiagent.create_layout()
pdf_uiagent.greet()

if st.session_state.message_hist == []:
    pdf_uiagent.initialize_conv(competency_analysis_agent.random_intro())
else:
    pdf_uiagent.show_conversation(st.session_state.message_hist)

# This is the user's textbox for chatting with the assistant
if prompt := st.chat_input("Quelle est votre question ?"):
    new_message = {"role": "user", "content": prompt}
    st.session_state.message_hist.append(new_message)
    pdf_uiagent.format_user_question(prompt)
    
    streamed_response = competency_analysis_agent.answer_rag(
            message_hist=st.session_state.message_hist[-2:], 
            user_question = prompt
        )
    full_str_reponse = pdf_uiagent.format_llm_response(streamed_response)

    st.session_state.message_hist.append(
        {"role": "assistant", "content": full_str_reponse}
    )