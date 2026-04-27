from comercio_eletronico import Cliente, Categoria, Produto
from dao import ClienteDAO, CategoriaDAO, ProdutoDAO


class UI:

    @staticmethod
    def Main() -> None:
        # Carrega dados salvos ao iniciar
        ClienteDAO.Abrir()
        CategoriaDAO.Abrir()
        ProdutoDAO.Abrir()

        while True:
            opcao = UI.Menu()

            # ── Produtos ──
            if opcao == 1:
                UI.Produto_Listar()
            elif opcao == 2:
                UI.Produto_Inserir()
            elif opcao == 3:
                UI.Produto_Atualizar()
            elif opcao == 4:
                UI.Produto_Excluir()

            # ── Categorias ──
            elif opcao == 5:
                UI.Categoria_Listar()
            elif opcao == 6:
                UI.Categoria_Inserir()
            elif opcao == 7:
                UI.Categoria_Atualizar()
            elif opcao == 8:
                UI.Categoria_Excluir()

            # ── Clientes ──
            elif opcao == 9:
                UI.Cliente_Listar()
            elif opcao == 10:
                UI.Cliente_Inserir()
            elif opcao == 11:
                UI.Cliente_Atualizar()
            elif opcao == 12:
                UI.Cliente_Excluir()

            # ── Sair ──
            elif opcao == 0:
                # Salva dados antes de encerrar
                ClienteDAO.Salvar()
                CategoriaDAO.Salvar()
                ProdutoDAO.Salvar()
                print("\nDados salvos. Encerrando o sistema. Até logo!")
                break

    @staticmethod
    def Menu() -> int:
        print("\n" + "=" * 40)
        print("   SISTEMA DE COMÉRCIO ELETRÔNICO")
        print("=" * 40)
        print(" --- PRODUTOS ---")
        print("  1. Listar Produtos")
        print("  2. Inserir Produto")
        print("  3. Atualizar Produto")
        print("  4. Excluir Produto")
        print(" --- CATEGORIAS ---")
        print("  5. Listar Categorias")
        print("  6. Inserir Categoria")
        print("  7. Atualizar Categoria")
        print("  8. Excluir Categoria")
        print(" --- CLIENTES ---")
        print("  9. Listar Clientes")
        print(" 10. Inserir Cliente")
        print(" 11. Atualizar Cliente")
        print(" 12. Excluir Cliente")
        print(" ---")
        print("  0. Finalizar")
        print("=" * 40)

        while True:
            try:
                opcao = int(input("Escolha uma opção: "))
                if 0 <= opcao <= 12:
                    return opcao
                print("Opção inválida. Digite um número entre 0 e 12.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    # ─────────────────────────────────────────
    # PRODUTO
    # ─────────────────────────────────────────
    @staticmethod
    def Produto_Listar() -> None:
        print("\n--- LISTA DE PRODUTOS ---")
        produtos = ProdutoDAO.Listar()
        if not produtos:
            print("Nenhum produto cadastrado.")
        else:
            for p in produtos:
                print(p)

    @staticmethod
    def Produto_Inserir() -> None:
        print("\n--- INSERIR PRODUTO ---")
        try:
            id = int(input("ID: "))
            if ProdutoDAO.Listar_Id(id):
                print("Erro: já existe um produto com este ID.")
                return
            descricao = input("Descrição: ")
            preco = float(input("Preço: "))
            estoque = int(input("Estoque: "))
            idCategoria = int(input("ID da Categoria: "))

            p = Produto(id, descricao, preco, estoque)
            p.set_idCategoria(idCategoria)
            ProdutoDAO.Inserir(p)
            print("Produto inserido com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Produto_Atualizar() -> None:
        print("\n--- ATUALIZAR PRODUTO ---")
        try:
            id = int(input("ID do produto a atualizar: "))
            p = ProdutoDAO.Listar_Id(id)
            if not p:
                print("Produto não encontrado.")
                return
            print(f"Produto atual: {p}")
            descricao = input(f"Nova descrição [{p.get_descricao()}]: ") or p.get_descricao()
            preco_str = input(f"Novo preço [{p.get_preco()}]: ")
            preco = float(preco_str) if preco_str else p.get_preco()
            estoque_str = input(f"Novo estoque [{p.get_estoque()}]: ")
            estoque = int(estoque_str) if estoque_str else p.get_estoque()
            idCat_str = input(f"Novo ID Categoria [{p.get_idCategoria()}]: ")
            idCategoria = int(idCat_str) if idCat_str else p.get_idCategoria()

            p.set_descricao(descricao)
            p.set_preco(preco)
            p.set_estoque(estoque)
            p.set_idCategoria(idCategoria)
            ProdutoDAO.Atualizar(p)
            print("Produto atualizado com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Produto_Excluir() -> None:
        print("\n--- EXCLUIR PRODUTO ---")
        try:
            id = int(input("ID do produto a excluir: "))
            p = ProdutoDAO.Listar_Id(id)
            if not p:
                print("Produto não encontrado.")
                return
            print(f"Produto: {p}")
            confirmacao = input("Confirma exclusão? (s/n): ")
            if confirmacao.lower() == "s":
                ProdutoDAO.Excluir(p)
                print("Produto excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
        except ValueError:
            print("Erro: entrada inválida.")

    # ─────────────────────────────────────────
    # CATEGORIA
    # ─────────────────────────────────────────
    @staticmethod
    def Categoria_Listar() -> None:
        print("\n--- LISTA DE CATEGORIAS ---")
        categorias = CategoriaDAO.Listar()
        if not categorias:
            print("Nenhuma categoria cadastrada.")
        else:
            for c in categorias:
                print(c)

    @staticmethod
    def Categoria_Inserir() -> None:
        print("\n--- INSERIR CATEGORIA ---")
        try:
            id = int(input("ID: "))
            if CategoriaDAO.Listar_Id(id):
                print("Erro: já existe uma categoria com este ID.")
                return
            descricao = input("Descrição: ")
            c = Categoria(id, descricao)
            CategoriaDAO.Inserir(c)
            print("Categoria inserida com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Categoria_Atualizar() -> None:
        print("\n--- ATUALIZAR CATEGORIA ---")
        try:
            id = int(input("ID da categoria a atualizar: "))
            c = CategoriaDAO.Listar_Id(id)
            if not c:
                print("Categoria não encontrada.")
                return
            print(f"Categoria atual: {c}")
            descricao = input(f"Nova descrição [{c.get_descricao()}]: ") or c.get_descricao()
            c.set_descricao(descricao)
            CategoriaDAO.Atualizar(c)
            print("Categoria atualizada com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Categoria_Excluir() -> None:
        print("\n--- EXCLUIR CATEGORIA ---")
        try:
            id = int(input("ID da categoria a excluir: "))
            c = CategoriaDAO.Listar_Id(id)
            if not c:
                print("Categoria não encontrada.")
                return
            print(f"Categoria: {c}")
            confirmacao = input("Confirma exclusão? (s/n): ")
            if confirmacao.lower() == "s":
                CategoriaDAO.Excluir(c)
                print("Categoria excluída com sucesso!")
            else:
                print("Exclusão cancelada.")
        except ValueError:
            print("Erro: entrada inválida.")

    # ─────────────────────────────────────────
    # CLIENTE
    # ─────────────────────────────────────────
    @staticmethod
    def Cliente_Listar() -> None:
        print("\n--- LISTA DE CLIENTES ---")
        clientes = ClienteDAO.Listar()
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for c in clientes:
                print(c)

    @staticmethod
    def Cliente_Inserir() -> None:
        print("\n--- INSERIR CLIENTE ---")
        try:
            id = int(input("ID: "))
            if ClienteDAO.Listar_Id(id):
                print("Erro: já existe um cliente com este ID.")
                return
            nome = input("Nome: ")
            email = input("E-mail: ")
            fone = input("Telefone: ")
            c = Cliente(id, nome, email, fone)
            ClienteDAO.Inserir(c)
            print("Cliente inserido com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Cliente_Atualizar() -> None:
        print("\n--- ATUALIZAR CLIENTE ---")
        try:
            id = int(input("ID do cliente a atualizar: "))
            c = ClienteDAO.Listar_Id(id)
            if not c:
                print("Cliente não encontrado.")
                return
            print(f"Cliente atual: {c}")
            nome = input(f"Novo nome [{c.get_nome()}]: ") or c.get_nome()
            email = input(f"Novo e-mail [{c.get_email()}]: ") or c.get_email()
            fone = input(f"Novo telefone [{c.get_fone()}]: ") or c.get_fone()
            c.set_nome(nome)
            c.set_email(email)
            c.set_fone(fone)
            ClienteDAO.Atualizar(c)
            print("Cliente atualizado com sucesso!")
        except ValueError:
            print("Erro: entrada inválida.")

    @staticmethod
    def Cliente_Excluir() -> None:
        print("\n--- EXCLUIR CLIENTE ---")
        try:
            id = int(input("ID do cliente a excluir: "))
            c = ClienteDAO.Listar_Id(id)
            if not c:
                print("Cliente não encontrado.")
                return
            print(f"Cliente: {c}")
            confirmacao = input("Confirma exclusão? (s/n): ")
            if confirmacao.lower() == "s":
                ClienteDAO.Excluir(c)
                print("Cliente excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
        except ValueError:
            print("Erro: entrada inválida.")


# ─────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────
if __name__ == "__main__":
    UI.Main()