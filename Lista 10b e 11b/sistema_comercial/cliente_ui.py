import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dados.banco import Banco
from modelos.usuario import Cliente, Admin
from modelos.carrinho import ItemCarrinho
from modelos.venda import Venda
from excecoes import ErroValidacao, ErroEstoqueInsuficiente, ErroQuantidadeInvalida

banco = Banco()

# Cliente de teste
if "joao" not in banco.usuarios:
    cliente_teste = Cliente(
        login="joao",
        senha="123",
        nome="Joao Silva",
        email="joao@email.com",
        telefone="84999999999",
        cpf="111.111.111-11",
        endereco="Rua A, 10"
    )
    banco.usuarios["joao"] = cliente_teste

def inicializar_sessao():
    if "cliente" not in st.session_state:
        st.session_state.cliente = None

def tela_login():
    st.header("Login do Cliente")
    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            usuario = banco.usuarios.get(login)
            if usuario is None:
                raise ErroValidacao("Usuario nao encontrado.")
            if not usuario.verificar_senha(senha):
                raise ErroValidacao("Senha incorreta.")
            if not isinstance(usuario, Cliente):
                raise ErroValidacao("Esse usuario nao e um cliente.")
            st.session_state.cliente = usuario
            st.rerun()
        except ErroValidacao as e:
            st.error(str(e))

def tela_cliente():
    cliente = st.session_state.cliente
    st.sidebar.write(f"Logado como: {cliente.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.cliente = None
        st.rerun()

    aba = st.tabs(["Listar Produtos", "Inserir no Carrinho", "Visualizar Carrinho", "Comprar Carrinho", "Minhas Compras"])

    with aba[0]:
        listar_produtos()
    with aba[1]:
        inserir_no_carrinho(cliente)
    with aba[2]:
        visualizar_carrinho(cliente)
    with aba[3]:
        comprar_carrinho(cliente)
    with aba[4]:
        listar_minhas_compras(cliente)

def listar_produtos():
    st.subheader("Produtos Disponiveis")
    try:
        produtos = [
            {
                "ID": p.id,
                "Nome": p.nome,
                "Preco": f"R${p.preco:.2f}",
                "Quantidade": p.quantidade,
                "Categoria": p.categoria.nome
            }
            for p in banco.produtos.values()
        ]
        if len(produtos) == 0:
            st.info("Nenhum produto cadastrado.")
        else:
            st.dataframe(produtos)
    except ErroValidacao as e:
        st.error(f"Erro ao listar produtos: {str(e)}")

def inserir_no_carrinho(cliente):
    st.subheader("Inserir Produto no Carrinho")
    try:
        if len(banco.produtos) == 0:
            st.info("Nenhum produto disponivel.")
            return

        opcoes = [f"{p.id} - {p.nome} - R${p.preco:.2f}" for p in banco.produtos.values()]
        selecionado = st.selectbox("Selecione o produto", opcoes)
        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        if st.button("Inserir no Carrinho"):
            if quantidade <= 0:
                raise ErroQuantidadeInvalida("A quantidade deve ser maior que zero.")

            id_produto = int(selecionado.split(" - ")[0])
            produto = banco.produtos.get(id_produto)

            if produto.quantidade == 0:
                raise ErroEstoqueInsuficiente(f"Produto {produto.nome} esta sem estoque.")

            for item in cliente.carrinho:
                if item.produto.id == produto.id:
                    item.quantidade += quantidade
                    st.success("Quantidade atualizada no carrinho!")
                    return

            novo_item = ItemCarrinho(produto, quantidade)
            cliente.carrinho.append(novo_item)
            st.success("Produto inserido no carrinho!")

    except ErroQuantidadeInvalida as e:
        st.error(f"Quantidade invalida: {str(e)}")
    except ErroEstoqueInsuficiente as e:
        st.error(f"Estoque insuficiente: {str(e)}")
    except ErroValidacao as e:
        st.error(str(e))

def visualizar_carrinho(cliente):
    st.subheader("Seu Carrinho")
    try:
        if len(cliente.carrinho) == 0:
            st.info("Carrinho vazio.")
            return

        itens = [
            {
                "Produto": item.produto.nome,
                "Preco Unitario": f"R${item.produto.preco:.2f}",
                "Quantidade": item.quantidade,
                "Total": f"R${item.produto.preco * item.quantidade:.2f}"
            }
            for item in cliente.carrinho
        ]
        st.dataframe(itens)
        total = sum(item.produto.preco * item.quantidade for item in cliente.carrinho)
        st.write(f"**Total geral: R${total:.2f}**")

    except ErroValidacao as e:
        st.error(str(e))

def comprar_carrinho(cliente):
    st.subheader("Comprar Carrinho")
    try:
        if len(cliente.carrinho) == 0:
            st.info("Carrinho vazio.")
            return

        visualizar_carrinho(cliente)

        if st.button("Confirmar Compra"):
            for item in cliente.carrinho:
                produto = banco.produtos.get(item.produto.id)
                if item.quantidade > produto.quantidade:
                    raise ErroEstoqueInsuficiente(
                        f"Estoque insuficiente para {produto.nome}. Disponivel: {produto.quantidade}"
                    )

            for item in cliente.carrinho:
                produto = banco.produtos.get(item.produto.id)
                produto.quantidade -= item.quantidade

            id_venda = banco.proximo_id_venda()
            nova_venda = Venda(id_venda, cliente, list(cliente.carrinho))
            banco.vendas.append(nova_venda)
            cliente.compras.append(nova_venda)
            cliente.carrinho = []
            st.success(f"Compra realizada! Total: R${nova_venda.total():.2f}")

    except ErroEstoqueInsuficiente as e:
        st.error(f"Erro no estoque: {str(e)}")
    except ErroValidacao as e:
        st.error(str(e))

def listar_minhas_compras(cliente):
    st.subheader("Minhas Compras")
    try:
        if len(cliente.compras) == 0:
            st.info("Voce ainda nao fez nenhuma compra.")
            return

        for venda in cliente.compras:
            st.write(f"**Venda #{venda.id} | Total: R${venda.total():.2f}**")
            itens = [
                {
                    "Produto": item.produto.nome,
                    "Quantidade": item.quantidade,
                    "Total": f"R${item.produto.preco * item.quantidade:.2f}"
                }
                for item in venda.itens
            ]
            st.dataframe(itens)

    except ErroValidacao as e:
        st.error(str(e))

inicializar_sessao()
if st.session_state.cliente is None:
    def tela_login():
      st.header("Acesso ao Sistema")
    aba = st.tabs(["Login", "Criar Conta"])

    with aba[0]:
        login = st.text_input("Login")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            try:
                usuario = banco.usuarios.get(login)
                if usuario is None:
                    raise ErroValidacao("Usuario nao encontrado.")
                if not usuario.verificar_senha(senha):
                    raise ErroValidacao("Senha incorreta.")
                if not isinstance(usuario, Cliente):
                    raise ErroValidacao("Esse usuario nao e um cliente.")
                st.session_state.cliente = usuario
                st.rerun()
            except ErroValidacao as e:
                st.error(str(e))

    with aba[1]:
        st.subheader("Criar Nova Conta")
        novo_login = st.text_input("Escolha um login")
        novo_nome = st.text_input("Nome completo")
        novo_email = st.text_input("E-mail")
        novo_fone = st.text_input("Telefone")
        novo_cpf = st.text_input("CPF")
        novo_endereco = st.text_input("Endereco")
        nova_senha = st.text_input("Senha", type="password", key="senha_cadastro")

        if st.button("Criar Conta"):
            try:
                if not novo_login or not novo_nome or not novo_email or not nova_senha:
                    raise ErroValidacao("Preencha todos os campos obrigatorios.")
                if novo_login in banco.usuarios:
                    raise ErroValidacao("Esse login ja esta em uso.")

                novo_cliente = Cliente(
                    login=novo_login,
                    senha=nova_senha,
                    nome=novo_nome,
                    email=novo_email,
                    telefone=novo_fone,
                    cpf=novo_cpf,
                    endereco=novo_endereco
                )
                banco.usuarios[novo_login] = novo_cliente
                st.success("Conta criada com sucesso! Faca o login.")
            except ErroValidacao as e:
                st.error(str(e))

# INICIO
inicializar_sessao()
if st.session_state.cliente is None:
    tela_login()
else:
    tela_cliente()