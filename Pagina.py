import streamlit as st
from analisador import *
from analista import *
from models import *
from database import *

usuarios = [elemento.nome for elemento in session.query(Usuario).all()]

selecao_usuario = st.selectbox(label="Selecione seu usuário",options=usuarios,index=None)
if selecao_usuario:
    produto = st.text_input(label='',placeholder='Insira o produto desejado')
    
    if produto:
    
        user = st.chat_message("user")
        user.write(produto)
        assistant = st.chat_message("assistant")
        assistant.write("Por favor, aguarde uns minutinhos enquanto a avaliação é feita")
        with st.spinner('Wait for it...'):
            result_function = pesquisar(produto)
            add_search(user=selecao_usuario,theme=f"{produto}",search=result_function['resposta'])
        st.info("Respota obtida")    
        bot = st.chat_message("ai")
        bot.write(result_function['resposta'])
        pop_over = st.popover(label="Faça o donwload do arquivo")
        with pop_over:
            download = st.download_button(
            label="Faça o download do checklist no formato Excel",
            data=convert_df_to_excel(result_function['pesquisa']),
            file_name= f"Pesquisa do produto {produto}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    





