import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import date
from dados.banco import Banco
from modelos.usuario import Admin
from modelos.produto import Produto, Categoria
from excecoes import ErroValidacao

banco = Banco()

if "admin" not in banco.usuarios:
    admin_padrao = Admin(
        login="admin",
        senha="admin123",
        nome="Administrador",
        email="admin@loja.com",
        telefone="(84) 99999-0000"
    )
    banco.usuarios["admin"] = admin_padrao

if len(banco.produtos) == 0:
    cat1 = Categoria(1, "Eletronicos")
    cat2 = Categoria(2, "Alimentos")
    cat3 = Categoria(3, "Vestuario")
    cat4 = Categoria(4, "Informatica")

    banco.categorias[1] = cat1
    banco.categorias[2] = cat2
    banco.categorias[3] = cat3
    banco.categorias[4] = cat4

    banco.produtos[1] = Produto(1, "Notebook", 2500.00, 10, cat1)
    banco.produtos[2] = Produto(2, "Smartphone", 1800.00, 15, cat1)
    banco.produtos[3] = Produto(3, "Mouse", 80.00, 50, cat4)
    banco.produtos[4] = Produto(4, "Arroz 5kg", 25.00, 100, cat2)
    banco.produtos[5] = Produto(5, "Camiseta", 49.00, 50, cat3)

def inicializar_sessao():
    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = None

def tela_login():
    st.header("Login do Administrador")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            usuario = banco.usuarios.get(login)
            if usuario is None:
                raise ErroValidacao("Usuario nao encontrado.")
            if not usuario.verificar_senha(senha):
                raise ErroValidacao("Senha incorreta.")
            if not isinstance(usuario, Admin):
                raise ErroValidacao("Esse usuario nao e um administrador.")
            st.session_state.admin_logado = usuario
            st.rerun()
        except ErroValidacao as e:
            st.error(str(e))

def tela_admin():
    st.sidebar.write(f"Logado como: {st.session_state.admin_logado.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.admin_logado = None
        st.rerun()

    st.header("Controle de Promocoes")
    aba = st.tabs(["Definir Promocao", "Produtos em Promocao"])

    with aba[0]:
        definir_promocao()
    with aba[1]:
        listar_promocoes()

def definir_promocao():
    st.subheader("Definir Promocao por Categoria")

    categorias = list(banco.categorias.values())
    if len(categorias) == 0:
        st.info("Nenhuma categoria cadastrada.")
        return

    opcoes = [f"{c.id} - {c.nome}" for c in categorias]
    selecionado = st.selectbox("Selecione a categoria", opcoes)

    desconto = st.number_input("Percentual de desconto (%)", min_value=1, max_value=100, step=1)
    inicio = st.date_input("Inicio da promocao", value=date.today())
    fim = st.date_input("Fim da promocao", value=date.today())

    if st.button("Ativar Promocao"):
        try:
            if fim < inicio:
                raise ErroValidacao("A data de fim deve ser maior que a data de inicio.")

            id_cat = int(selecionado.split(" - ")[0])
            categoria = banco.categorias.get(id_cat)
            categoria.promocao_ativa = True
            categoria.desconto = desconto
            categoria.inicio_promocao = inicio
            categoria.fim_promocao = fim

            st.success(f"Promocao de {desconto}% ativada para {categoria.nome} até {fim}!")
        except ErroValidacao as e:
            st.error(str(e))

    if st.button("Desativar Promocao"):
        id_cat = int(selecionado.split(" - ")[0])
        categoria = banco.categorias.get(id_cat)
        categoria.promocao_ativa = False
        categoria.desconto = 0
        st.success(f"Promocao desativada para {categoria.nome}!")

def listar_promocoes():
    st.subheader("Produtos em Promocao")

    produtos_promocao = [
        p for p in banco.produtos.values()
        if p.categoria.promocao_ativa
    ]

    if len(produtos_promocao) == 0:
        st.info("Nenhum produto em promocao no momento.")
        return

    for produto in produtos_promocao:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**{produto.nome}**")
            st.write(f"Categoria: {produto.categoria.nome}")
            st.write(f"Preco original: R${produto.preco:.2f}")
            st.write(f"Desconto: {produto.categoria.desconto}%")
        with col2:
            preco_final = produto.preco_com_desconto()
            st.metric("Preco com desconto", f"R${preco_final:.2f}")
        st.divider()

inicializar_sessao()
if st.session_state.admin_logado is None:
    tela_login()
else:
    tela_admin()