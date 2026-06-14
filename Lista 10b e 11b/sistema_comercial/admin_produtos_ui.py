import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dados.banco import Banco
from modelos.usuario import Admin
from excecoes import ErroValidacao

banco = Banco()

from modelos.produto import Produto, Categoria

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
    banco.produtos[3] = Produto(3, "Televisao 50pol", 3200.00, 8, cat1)
    banco.produtos[4] = Produto(4, "Fone de Ouvido", 150.00, 30, cat1)
    banco.produtos[5] = Produto(5, "Mouse", 80.00, 50, cat4)
    banco.produtos[6] = Produto(6, "Teclado", 120.00, 40, cat4)
    banco.produtos[7] = Produto(7, "Arroz 5kg", 25.00, 100, cat2)
    banco.produtos[8] = Produto(8, "Feijao 1kg", 10.00, 100, cat2)
    banco.produtos[9] = Produto(9, "Camiseta", 49.00, 50, cat3)
    banco.produtos[10] = Produto(10, "Calca Jeans", 120.00, 30, cat3)

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

    st.header("Gerenciar Produtos")
    aba = st.tabs(["Listar Produtos", "Adicionar Imagem"])

    with aba[0]:
        listar_produtos()
    with aba[1]:
        adicionar_imagem()

def listar_produtos():
    st.subheader("Produtos Cadastrados")

    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    for produto in banco.produtos.values():
        col1, col2 = st.columns([1, 3])
        with col1:
            if produto.imagem is not None:
                st.image(produto.imagem, width=100)
            else:
                st.write("Sem imagem")
        with col2:
            st.write(f"**{produto.nome}**")
            st.write(f"Preco: R${produto.preco:.2f}")
            st.write(f"Quantidade: {produto.quantidade}")
            st.write(f"Categoria: {produto.categoria.nome}")
        st.divider()

def adicionar_imagem():
    st.subheader("Adicionar Imagem ao Produto")

    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return

    opcoes = [f"{p.id} - {p.nome}" for p in banco.produtos.values()]
    selecionado = st.selectbox("Selecione o produto", opcoes)
    imagem = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])

    if st.button("Salvar Imagem"):
        try:
            if imagem is None:
                raise ErroValidacao("Selecione uma imagem.")
            id_produto = int(selecionado.split(" - ")[0])
            produto = banco.produtos.get(id_produto)
            produto.imagem = imagem.read()
            st.success(f"Imagem adicionada ao produto {produto.nome}!")
        except ErroValidacao as e:
            st.error(str(e))

inicializar_sessao()
if st.session_state.admin_logado is None:
    tela_login()
else:
    tela_admin()