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

        self.banco.categorias[1] = cat1
        self.banco.categorias[2] = cat2

        p1 = Produto(1, "Notebook", 2500.00, 10, cat1)
        p2 = Produto(2, "Mouse", 80.00, 50, cat1)
        p3 = Produto(3, "Arroz 5kg", 25.00, 100, cat2)
        p4 = Produto(4, "Feijao 1kg", 10.00, 100, cat2)

        self.banco.produtos[1] = p1
        self.banco.produtos[2] = p2
        self.banco.produtos[3] = p3
        self.banco.produtos[4] = p4

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
        if nome in produto.nome.lower():
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