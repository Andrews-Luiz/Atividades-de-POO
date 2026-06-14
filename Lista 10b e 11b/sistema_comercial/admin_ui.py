import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import datetime
from dados.banco import Banco
from modelos.usuario import Admin

banco = Banco()

# Admin padrão
from modelos.usuario import Admin
if "admin" not in banco.usuarios:
    admin_padrao = Admin(
        login="admin",
        senha="admin123",
        nome="Administrador",
        email="admin@loja.com",
        telefone="(84) 99999-0000"
    )
    banco.usuarios["admin"] = admin_padrao

def inicializar_sessao():
    if "admin" not in st.session_state:
        st.session_state.admin = None

def tela_login():
    st.header("Login do Administrador")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = banco.usuarios.get(login)
        if usuario is None:
            st.error("Usuario nao encontrado.")
        elif not usuario.verificar_senha(senha):
            st.error("Senha incorreta.")
        elif not isinstance(usuario, Admin):
            st.error("Esse usuario nao e um administrador.")
        else:
            st.session_state.admin = usuario
            st.rerun()

def tela_admin():
    st.sidebar.write(f"Logado como: {st.session_state.admin.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.admin = None
        st.rerun()

    st.header("Listar Vendas")

    if len(banco.vendas) == 0:
        st.info("Nenhuma venda realizada ainda.")
        return

    for venda in banco.vendas:
        st.write(f"**Venda #{venda.id} | Cliente: {venda.cliente.nome} | Total: R${venda.total():.2f}**")
        itens = [
            {
                "Produto": item.produto.nome,
                "Quantidade": item.quantidade,
                "Preco Unitario": f"R${item.produto.preco:.2f}",
                "Total": f"R${item.produto.preco * item.quantidade:.2f}"
            }
            for item in venda.itens
        ]
        st.dataframe(itens)
        st.divider()

inicializar_sessao()
if st.session_state.admin is None:
    tela_login()
else:
    tela_admin()