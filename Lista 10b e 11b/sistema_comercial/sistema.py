from dados.banco import Banco
from modelos.usuario import Cliente, Admin
from modelos.produto import Produto, Categoria
from modelos.carrinho import ItemCarrinho
from modelos.venda import Venda


class Sistema:
    def __init__(self):
        self.banco = Banco()
        self.usuario_logado = None
        self._criar_admin_padrao()
        self._criar_produtos_exemplo()

    def _criar_admin_padrao(self):
        admin = Admin(
            login="admin",
            senha="admin123",
            nome="Administrador",
            email="admin@loja.com",
            telefone="(84) 99999-0000"
        )
        self.banco.usuarios["admin"] = admin

    def _criar_produtos_exemplo(self):
        cat1 = Categoria(1, "Eletronicos")
        cat2 = Categoria(2, "Alimentos")
        cat3 = Categoria(3, "Vestuario")
        cat4 = Categoria(4, "Informatica")

        self.banco.categorias[1] = cat1
        self.banco.categorias[2] = cat2
        self.banco.categorias[3] = cat3
        self.banco.categorias[4] = cat4

        p1 = Produto(1, "Notebook", 2500.00, 10, cat1)
        p2 = Produto(2, "Smartphone", 1800.00, 15, cat1)
        p3 = Produto(3, "Televisao 50pol", 3200.00, 8, cat1)
        p4 = Produto(4, "Fone de Ouvido", 150.00, 30, cat1)
        p5 = Produto(5, "Mouse", 80.00, 50, cat4)
        p6 = Produto(6, "Teclado", 120.00, 40, cat4)
        p7 = Produto(7, "Pendrive 64GB", 45.00, 60, cat4)
        p8 = Produto(8, "Arroz 5kg", 25.00, 100, cat2)
        p9 = Produto(9, "Feijao 1kg", 10.00, 100, cat2)
        p10 = Produto(10, "Cafe 500g", 18.00, 80, cat2)
        p11 = Produto(11, "Camiseta", 49.00, 50, cat3)
        p12 = Produto(12, "Calca Jeans", 120.00, 30, cat3)
        p13 = Produto(13, "Geladeira", 2800.00, 5, cat1)
        p14 = Produto(14, "Micro-ondas", 600.00, 12, cat1)
        p15 = Produto(15, "Headset Gamer", 250.00, 25, cat4)
        p16 = Produto(16, "Webcam HD", 180.00, 20, cat4)
        p17 = Produto(17, "Oleo de Soja 900ml", 8.00, 150, cat2)
        p18 = Produto(18, "Macarrao 500g", 5.00, 200, cat2)
        p19 = Produto(19, "Tenis Casual", 180.00, 35, cat3)
        p20 = Produto(20, "Jaqueta", 220.00, 20, cat3)

        self.banco.produtos[1] = p1
        self.banco.produtos[2] = p2
        self.banco.produtos[3] = p3
        self.banco.produtos[4] = p4
        self.banco.produtos[5] = p5
        self.banco.produtos[6] = p6
        self.banco.produtos[7] = p7
        self.banco.produtos[8] = p8
        self.banco.produtos[9] = p9
        self.banco.produtos[10] = p10
        self.banco.produtos[11] = p11
        self.banco.produtos[12] = p12
        self.banco.produtos[13] = p13
        self.banco.produtos[14] = p14
        self.banco.produtos[15] = p15
        self.banco.produtos[16] = p16
        self.banco.produtos[17] = p17
        self.banco.produtos[18] = p18
        self.banco.produtos[19] = p19
        self.banco.produtos[20] = p20

    def menu_visitante(self):
        while True:
            print("\nMenu:")
            print("1. Entrar no sistema")
            print("2. Abrir conta")
            print("0. Sair")

            opcao = input("Opcao: ").strip()

            if opcao == "1":
                self.entrar_no_sistema()
            elif opcao == "2":
                self.abrir_conta()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opcao invalida.")

    def entrar_no_sistema(self):
        print("\nEntrar no sistema")
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()

        usuario = self.banco.usuarios.get(login)

        if usuario is None:
            print("Usuario nao encontrado.")
            return

        if not usuario.verificar_senha(senha):
            print("Senha incorreta.")
            return

        self.usuario_logado = usuario
        print("Bem-vindo(a), " + usuario.nome + "!")

        if isinstance(usuario, Admin):
            self.menu_admin()
        elif isinstance(usuario, Cliente):
            self.menu_cliente()

        self.usuario_logado = None

    def abrir_conta(self):
        print("\nCriar nova conta")

        login = input("Login: ").strip()
        if login in self.banco.usuarios:
            print("Esse login ja esta em uso.")
            return

        senha = input("Senha: ").strip()
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        telefone = input("Telefone: ").strip()
        cpf = input("CPF: ").strip()
        endereco = input("Endereco: ").strip()

        novo_cliente = Cliente(
            login=login,
            senha=senha,
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf,
            endereco=endereco
        )

        self.banco.usuarios[login] = novo_cliente
        print("Conta criada com sucesso!")

    def menu_cliente(self):
        while True:
            print("\nMenu Cliente:")
            print("1. Listar produtos")
            print("2. Inserir produto no carrinho")
            print("3. Visualizar carrinho")
            print("4. Comprar carrinho")
            print("5. Listar minhas compras")
            print("6. Buscar produto por nome")
            print("7. Limpar carrinho")
            print("0. Sair")

            opcao = input("Opcao: ").strip()

            if opcao == "1":
                self.listar_produtos()
            elif opcao == "2":
                self.inserir_no_carrinho()
            elif opcao == "3":
                self.visualizar_carrinho()
            elif opcao == "4":
                self.comprar_carrinho()
            elif opcao == "5":
                self.listar_minhas_compras()
            elif opcao == "6":
                self.buscar_produto_por_nome()
            elif opcao == "7":
                self.limpar_carrinho()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opcao invalida.")

    def menu_admin(self):
        while True:
            print("\nMenu Admin:")
            print("1. Listar vendas")
            print("0. Sair")

            opcao = input("Opcao: ").strip()

            if opcao == "1":
                self.listar_vendas()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opcao invalida.")

    def listar_produtos(self):
        print("\nProdutos disponiveis:")

        if len(self.banco.produtos) == 0:
            print("Nenhum produto cadastrado.")
            return

        for produto in self.banco.produtos.values():
            print(produto)
    def buscar_produto_por_nome(self):
        nome = input("Digite o nome do produto: ").strip().lower()

        encontrados = []
        for produto in self.banco.produtos.values():
            nome_produto = produto.nome.lower()
            if nome in nome_produto:
                encontrados.append(produto)

        if len(encontrados) == 0:
            print("Nenhum produto encontrado.")
            return

        print("\nProdutos encontrados:")
        for produto in encontrados:
            print(produto)

    def inserir_no_carrinho(self):
        self.listar_produtos()

        id_produto = input("\nDigite o ID do produto: ").strip()

        produto = self.banco.produtos.get(int(id_produto))
        if produto is None:
            print("Produto nao encontrado.")
            return

        quantidade = int(input("Digite a quantidade: ").strip())

        carrinho = self.usuario_logado.carrinho

        for item in carrinho:
            if item.produto.id == produto.id:
                item.quantidade += quantidade
                print("Quantidade atualizada no carrinho.")
                return

        novo_item = ItemCarrinho(produto, quantidade)
        carrinho.append(novo_item)
        print("Produto inserido no carrinho!")

    def visualizar_carrinho(self):
        carrinho = self.usuario_logado.carrinho

        if len(carrinho) == 0:
            print("Carrinho vazio.")
            return

        print("\nSeu carrinho:")
        total_geral = 0
        for item in carrinho:
            print(item)
            total_geral += item.produto.preco * item.quantidade

        print(f"Total geral: R${total_geral:.2f}")

    def comprar_carrinho(self):
        carrinho = self.usuario_logado.carrinho

        if len(carrinho) == 0:
            print("Carrinho vazio.")
            return

        for item in carrinho:
            produto = self.banco.produtos.get(item.produto.id)
            if item.quantidade > produto.quantidade:
                print(f"Quantidade insuficiente em estoque para: {produto.nome}")
                print(f"Disponivel: {produto.quantidade}")
                return

        for item in carrinho:
            produto = self.banco.produtos.get(item.produto.id)
            produto.quantidade -= item.quantidade

        id_venda = self.banco.proximo_id_venda()
        nova_venda = Venda(id_venda, self.usuario_logado, list(carrinho))

        self.banco.vendas.append(nova_venda)
        self.usuario_logado.compras.append(nova_venda)

        self.usuario_logado.carrinho = []
        print("Compra realizada com sucesso!")
        print(f"Total pago: R${nova_venda.total():.2f}")

    def listar_minhas_compras(self):
        compras = self.usuario_logado.compras

        if len(compras) == 0:
            print("Voce ainda nao fez nenhuma compra.")
            return

        print("\nSuas compras:")
        for venda in compras:
            print(venda)

    def listar_vendas(self):
        if len(self.banco.vendas) == 0:
            print("Nenhuma venda realizada.")
            return

        print("\nTodas as vendas:")
        for venda in self.banco.vendas:
            print(venda)

    def limpar_carrinho(self):
        self.usuario_logado.carrinho = []
        print("Carrinho limpo com sucesso!")