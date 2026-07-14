import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from datetime import date
from dados.banco import Banco
from modelos.usuario import Cliente, Admin, Entregador
from modelos.produto import Produto, Categoria
from modelos.carrinho import ItemCarrinho
from modelos.venda import Venda
from modelos.entrega import Entrega
from excecoes import ErroValidacao, ErroEstoqueInsuficiente, ErroQuantidadeInvalida

banco = Banco()

if "admin" not in banco.usuarios:
    banco.usuarios["admin"] = Admin("admin", "admin123", "Administrador", "admin@loja.com", "(84) 99999-0000")

if len(banco.produtos) == 0:
    cat1 = Categoria(1, "Eletronicos")
    cat2 = Categoria(2, "Alimentos")
    cat3 = Categoria(3, "Vestuario")
    cat4 = Categoria(4, "Informatica")
    banco.categorias[1] = cat1
    banco.categorias[2] = cat2
    banco.categorias[3] = cat3
    banco.categorias[4] = cat4
    banco.produtos[1]  = Produto(1,  "Notebook",        2500.00, 10,  cat1, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=200")
    banco.produtos[2]  = Produto(2,  "Smartphone",      1800.00, 15,  cat1, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=200")
    banco.produtos[3]  = Produto(3,  "Televisao 50pol", 3200.00, 8,   cat1, "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=200")
    banco.produtos[4]  = Produto(4,  "Fone de Ouvido",  150.00,  30,  cat1, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=200")
    banco.produtos[5]  = Produto(5,  "Mouse",           80.00,   50,  cat4, "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=200")
    banco.produtos[6]  = Produto(6,  "Teclado",         120.00,  40,  cat4, "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=200")
    banco.produtos[7]  = Produto(7,  "Pendrive 64GB",   45.00,   60,  cat4, "https://images.unsplash.com/photo-1618410320928-25228d811631?w=200")
    banco.produtos[8]  = Produto(8,  "Arroz 5kg",       25.00,   100, cat2, "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200")
    banco.produtos[9]  = Produto(9,  "Feijao 1kg",      10.00,   100, cat2, "https://images.unsplash.com/photo-1612257999756-54cf1b5f80cc?w=200")
    banco.produtos[10] = Produto(10, "Cafe 500g",       18.00,   80,  cat2, "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=200")
    banco.produtos[11] = Produto(11, "Camiseta",        49.00,   50,  cat3, "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200")
    banco.produtos[12] = Produto(12, "Calca Jeans",     120.00,  30,  cat3, "https://images.unsplash.com/photo-1542272604-787c3835535d?w=200")

def inicializar_sessao():
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
    if "tipo" not in st.session_state:
        st.session_state.tipo = None

def tela_inicial():
    st.title("Loja Virtual")
    aba = st.tabs(["Login", "Criar Conta", "Cadastro de Entregador"])

    with aba[0]:
        st.subheader("Login")
        login = st.text_input("Login", key="login_login")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar"):
            try:
                usuario = banco.usuarios.get(login)
                if usuario is None:
                    raise ErroValidacao("Usuario nao encontrado.")
                if not usuario.verificar_senha(senha):
                    raise ErroValidacao("Senha incorreta.")
                st.session_state.usuario = usuario
                if isinstance(usuario, Admin):
                    st.session_state.tipo = "admin"
                elif isinstance(usuario, Entregador):
                    st.session_state.tipo = "entregador"
                else:
                    st.session_state.tipo = "cliente"
                st.rerun()
            except ErroValidacao as e:
                st.error(str(e))

    with aba[1]:
        st.subheader("Criar Nova Conta")
        novo_login    = st.text_input("Login", key="cadastro_login")
        novo_nome     = st.text_input("Nome completo", key="cadastro_nome")
        novo_email    = st.text_input("E-mail", key="cadastro_email")
        novo_fone     = st.text_input("Telefone", key="cadastro_fone")
        novo_cpf      = st.text_input("CPF", key="cadastro_cpf")
        novo_endereco = st.text_input("Endereco", key="cadastro_endereco")
        nova_senha    = st.text_input("Senha", type="password", key="cadastro_senha")

        if st.button("Criar Conta"):
            try:
                if not novo_login or not novo_nome or not novo_email or not nova_senha:
                    raise ErroValidacao("Preencha todos os campos obrigatorios.")
                if novo_login in banco.usuarios:
                    raise ErroValidacao("Esse login ja esta em uso.")
                novo_cliente = Cliente(novo_login, nova_senha, novo_nome, novo_email, novo_fone, novo_cpf, novo_endereco)
                banco.usuarios[novo_login] = novo_cliente
                st.success("Conta criada com sucesso! Faca o login.")
            except ErroValidacao as e:
                st.error(str(e))

    with aba[2]:
        st.subheader("Cadastro de Entregador")
        e_login  = st.text_input("Login", key="ent_login")
        e_nome   = st.text_input("Nome completo", key="ent_nome")
        e_email  = st.text_input("E-mail", key="ent_email")
        e_fone   = st.text_input("Telefone", key="ent_fone")
        e_veiculo= st.text_input("Veiculo (ex: Moto, Carro)", key="ent_veiculo")
        e_senha  = st.text_input("Senha", type="password", key="ent_senha")

        if st.button("Cadastrar como Entregador"):
            try:
                if not e_login or not e_nome or not e_email or not e_senha or not e_veiculo:
                    raise ErroValidacao("Preencha todos os campos obrigatorios.")
                if e_login in banco.usuarios:
                    raise ErroValidacao("Esse login ja esta em uso.")
                novo_entregador = Entregador(e_login, e_senha, e_nome, e_email, e_fone, e_veiculo)
                banco.usuarios[e_login] = novo_entregador
                st.success("Entregador cadastrado com sucesso! Faca o login.")
            except ErroValidacao as e:
                st.error(str(e))

# ─────────────────────────────────────────
# AREA DO CLIENTE
# ─────────────────────────────────────────
def area_cliente():
    cliente = st.session_state.usuario
    st.sidebar.write(f"Logado como: {cliente.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.session_state.tipo = None
        st.rerun()

    aba = st.tabs(["Listar Produtos", "Inserir no Carrinho", "Visualizar Carrinho", "Comprar Carrinho", "Minhas Compras", "Minhas Entregas"])

    with aba[0]:
        listar_produtos_cliente()
    with aba[1]:
        inserir_no_carrinho(cliente)
    with aba[2]:
        visualizar_carrinho(cliente)
    with aba[3]:
        comprar_carrinho(cliente)
    with aba[4]:
        listar_minhas_compras(cliente)
    with aba[5]:
        minhas_entregas(cliente)

def listar_produtos_cliente():
    st.subheader("Produtos Disponiveis")
    try:
        if len(banco.produtos) == 0:
            st.info("Nenhum produto cadastrado.")
            return
        for produto in banco.produtos.values():
            col1, col2 = st.columns([1, 3])
            with col1:
                if produto.imagem is not None:
                    st.image(produto.imagem, width=100)
            with col2:
                st.write(f"**{produto.nome}**")
                st.write(f"Categoria: {produto.categoria.nome}")
                if produto.categoria.promocao_ativa:
                    st.write(f"~~R${produto.preco:.2f}~~")
                    st.write(f"**Preco com desconto: R${produto.preco_com_desconto():.2f}**")
                    st.write(f"Desconto: {produto.categoria.desconto}%")
                else:
                    st.write(f"Preco: R${produto.preco:.2f}")
                st.write(f"Quantidade disponivel: {produto.quantidade}")
            st.divider()
    except ErroValidacao as e:
        st.error(str(e))

def inserir_no_carrinho(cliente):
    st.subheader("Inserir Produto no Carrinho")
    try:
        if len(banco.produtos) == 0:
            st.info("Nenhum produto disponivel.")
            return
        opcoes = [f"{p.id} - {p.nome} - R${p.preco_com_desconto():.2f}" for p in banco.produtos.values()]
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
                "Preco Unitario": f"R${item.produto.preco_com_desconto():.2f}",
                "Quantidade": item.quantidade,
                "Total": f"R${item.produto.preco_com_desconto() * item.quantidade:.2f}"
            }
            for item in cliente.carrinho
        ]
        st.dataframe(itens)
        total = sum(item.produto.preco_com_desconto() * item.quantidade for item in cliente.carrinho)
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
                    raise ErroEstoqueInsuficiente(f"Estoque insuficiente para {produto.nome}. Disponivel: {produto.quantidade}")
            for item in cliente.carrinho:
                produto = banco.produtos.get(item.produto.id)
                produto.quantidade -= item.quantidade
            id_venda = banco.proximo_id_venda()
            total_com_desconto = sum(item.produto.preco_com_desconto() * item.quantidade for item in cliente.carrinho)
            nova_venda = Venda(id_venda, cliente, list(cliente.carrinho))
            banco.vendas.append(nova_venda)
            cliente.compras.append(nova_venda)
            cliente.carrinho = []
            st.success(f"Compra realizada! Total: R${total_com_desconto:.2f}")
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
            itens = [{"Produto": item.produto.nome, "Quantidade": item.quantidade, "Total": f"R${item.produto.preco_com_desconto() * item.quantidade:.2f}"} for item in venda.itens]
            st.dataframe(itens)
    except ErroValidacao as e:
        st.error(str(e))

def minhas_entregas(cliente):
    st.subheader("Status das Minhas Entregas")
    entregas = [e for e in banco.entregas.values() if e.venda.cliente.login == cliente.login]
    if len(entregas) == 0:
        st.info("Nenhuma entrega encontrada.")
        return
    for entrega in entregas:
        st.write(f"**Entrega #{entrega.id} | Venda #{entrega.venda.id}**")
        st.write(f"Entregador: {entrega.entregador.nome} | Veiculo: {entrega.entregador.veiculo}")
        st.write(f"Status: **{entrega.status}**")
        st.divider()

# ─────────────────────────────────────────
# AREA DO ENTREGADOR
# ─────────────────────────────────────────
def area_entregador():
    entregador = st.session_state.usuario
    st.sidebar.write(f"Logado como: {entregador.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.session_state.tipo = None
        st.rerun()

    st.header("Minhas Entregas")
    entregas = [e for e in banco.entregas.values() if e.entregador.login == entregador.login]

    if len(entregas) == 0:
        st.info("Nenhuma entrega alocada para voce ainda.")
        return

    for entrega in entregas:
        st.write(f"**Entrega #{entrega.id} | Venda #{entrega.venda.id} | Cliente: {entrega.venda.cliente.nome}**")
        st.write(f"Status atual: **{entrega.status}**")

        novo_status = st.selectbox(
            "Atualizar status",
            ["Pendente", "Em entrega", "Entregue"],
            index=["Pendente", "Em entrega", "Entregue"].index(entrega.status),
            key=f"status_{entrega.id}"
        )

        if st.button("Salvar", key=f"salvar_{entrega.id}"):
            entrega.status = novo_status
            st.success("Status atualizado!")
        st.divider()

# ─────────────────────────────────────────
# AREA DO ADMIN
# ─────────────────────────────────────────
def area_admin():
    st.sidebar.write(f"Logado como: {st.session_state.usuario.nome}")
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.session_state.tipo = None
        st.rerun()

    aba = st.tabs(["Listar Vendas", "Gerenciar Entregas", "Gerenciar Produtos", "Promocoes", "Imagens"])

    with aba[0]:
        listar_vendas()
    with aba[1]:
        gerenciar_entregas()
    with aba[2]:
        gerenciar_produtos()
    with aba[3]:
        gerenciar_promocoes()
    with aba[4]:
        gerenciar_imagens()

def listar_vendas():
    st.subheader("Todas as Vendas")
    if len(banco.vendas) == 0:
        st.info("Nenhuma venda realizada ainda.")
        return
    for venda in banco.vendas:
        st.write(f"**Venda #{venda.id} | Cliente: {venda.cliente.nome} | Total: R${venda.total():.2f}**")
        itens = [{"Produto": item.produto.nome, "Quantidade": item.quantidade, "Total": f"R${item.produto.preco * item.quantidade:.2f}"} for item in venda.itens]
        st.dataframe(itens)
        st.divider()

def gerenciar_entregas():
    st.subheader("Alocar Entregador para Venda")

    if len(banco.vendas) == 0:
        st.info("Nenhuma venda realizada ainda.")
        return

    entregadores = [u for u in banco.usuarios.values() if isinstance(u, Entregador)]
    if len(entregadores) == 0:
        st.warning("Nenhum entregador cadastrado.")
        return

    opcoes_vendas = [f"Venda #{v.id} - {v.cliente.nome}" for v in banco.vendas]
    selecionado_venda = st.selectbox("Selecione a venda", opcoes_vendas, key="select_venda")

    opcoes_entregadores = [f"{e.login} - {e.nome} - {e.veiculo}" for e in entregadores]
    selecionado_entregador = st.selectbox("Selecione o entregador", opcoes_entregadores, key="select_entregador")

    if st.button("Alocar Entregador"):
        id_venda = int(selecionado_venda.split("#")[1].split(" ")[0])
        login_entregador = selecionado_entregador.split(" - ")[0]

        venda = next(v for v in banco.vendas if v.id == id_venda)
        entregador = banco.usuarios.get(login_entregador)

        id_entrega = banco.proximo_id_entrega()
        nova_entrega = Entrega(id_entrega, venda, entregador)
        banco.entregas[id_entrega] = nova_entrega
        entregador.entregas.append(nova_entrega)
        st.success(f"Entregador {entregador.nome} alocado para a Venda #{id_venda}!")

    st.divider()
    st.subheader("Entregas em Andamento")
    if len(banco.entregas) == 0:
        st.info("Nenhuma entrega criada ainda.")
        return
    for entrega in banco.entregas.values():
        st.write(f"Entrega #{entrega.id} | Venda #{entrega.venda.id} | Entregador: {entrega.entregador.nome} | Status: **{entrega.status}**")

def gerenciar_produtos():
    st.subheader("Produtos Cadastrados")
    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return
    for produto in banco.produtos.values():
        col1, col2 = st.columns([1, 3])
        with col1:
            if produto.imagem is not None:
                st.image(produto.imagem, width=100)
        with col2:
            st.write(f"**{produto.nome}**")
            st.write(f"Preco: R${produto.preco:.2f}")
            st.write(f"Quantidade: {produto.quantidade}")
            st.write(f"Categoria: {produto.categoria.nome}")
        st.divider()

def gerenciar_promocoes():
    st.subheader("Controle de Promocoes")
    aba = st.tabs(["Definir Promocao", "Produtos em Promocao"])
    with aba[0]:
        definir_promocao()
    with aba[1]:
        listar_promocoes()

def gerenciar_imagens():
    st.subheader("Gerenciar Imagens dos Produtos")
    if len(banco.produtos) == 0:
        st.info("Nenhum produto cadastrado.")
        return
    opcoes = [f"{p.id} - {p.nome}" for p in banco.produtos.values()]
    selecionado = st.selectbox("Selecione o produto", opcoes, key="select_imagem")
    imagem = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg"])
    if st.button("Salvar Imagem"):
        try:
            if imagem is None:
                raise ErroValidacao("Selecione uma imagem.")
            id_produto = int(selecionado.split(" - ")[0])
            produto = banco.produtos.get(id_produto)
            produto.imagem = imagem.read()
            st.success(f"Imagem atualizada para {produto.nome}!")
        except ErroValidacao as e:
            st.error(str(e))

def definir_promocao():
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
            st.success(f"Promocao de {desconto}% ativada para {categoria.nome} ate {fim}!")
        except ErroValidacao as e:
            st.error(str(e))
    if st.button("Desativar Promocao"):
        id_cat = int(selecionado.split(" - ")[0])
        categoria = banco.categorias.get(id_cat)
        categoria.promocao_ativa = False
        categoria.desconto = 0
        st.success(f"Promocao desativada para {categoria.nome}!")

def listar_promocoes():
    produtos_promocao = [p for p in banco.produtos.values() if p.categoria.promocao_ativa]
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
            st.metric("Preco com desconto", f"R${produto.preco_com_desconto():.2f}")
        st.divider()

# ─────────────────────────────────────────
# INICIO
# ─────────────────────────────────────────
inicializar_sessao()

if st.session_state.usuario is None:
    tela_inicial()
elif st.session_state.tipo == "cliente":
    area_cliente()
elif st.session_state.tipo == "admin":
    area_admin()
elif st.session_state.tipo == "entregador":
    area_entregador()     