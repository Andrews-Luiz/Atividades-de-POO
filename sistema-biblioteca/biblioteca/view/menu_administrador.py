from service.categoria_service import CategoriaService
from service.autor_service import AutorService
from service.editora_service import EditoraService
from service.livro_service import LivroService
from service.usuario_service import UsuarioService
from service.emprestimo_service import EmprestimoService
from model.usuario import Usuario


def menu_administrador(usuario_logado):
    categoria_service = CategoriaService()
    autor_service = AutorService()
    editora_service = EditoraService()
    livro_service = LivroService()
    usuario_service = UsuarioService()
    emprestimo_service = EmprestimoService()

    while True:
        print(f"\n=== MENU ADMINISTRADOR ({usuario_logado.nome}) ===")
        print("1 - Gerenciar Categorias")
        print("2 - Gerenciar Autores")
        print("3 - Gerenciar Editoras")
        print("4 - Gerenciar Livros")
        print("5 - Gerenciar Usuários")
        print("6 - Vincular Livro a Categoria / Autor / Editora")
        print("7 - Pesquisar Livro por título")
        print("8 - Listar todos os Empréstimos")
        print("9 - Registrar Devolução")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            _menu_categorias(categoria_service)
        elif opcao == "2":
            _menu_autores(autor_service)
        elif opcao == "3":
            _menu_editoras(editora_service)
        elif opcao == "4":
            _menu_livros(livro_service)
        elif opcao == "5":
            _menu_usuarios(usuario_service)
        elif opcao == "6":
            _vincular_livro(livro_service)
        elif opcao == "7":
            _pesquisar_livro(livro_service)
        elif opcao == "8":
            for e in emprestimo_service.listar():
                print(e)
        elif opcao == "9":
            _registrar_devolucao(emprestimo_service)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def _menu_categorias(categoria_service):
    print("\n-- Categorias --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        desc = input("Descrição: ")
        print(categoria_service.cadastrar(nome, desc))
    elif op == "2":
        for c in categoria_service.listar():
            print(c)
    elif op == "3":
        id = int(input("ID da categoria: "))
        c = categoria_service.buscar_por_id(id)
        if c:
            c.nome = input(f"Novo nome ({c.nome}): ") or c.nome
            categoria_service.atualizar(c)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID da categoria: "))
        print("Excluído!" if categoria_service.excluir(id) else "Não encontrado.")


def _menu_autores(autor_service):
    print("\n-- Autores --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir 5-Pesquisar por nome")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        nacionalidade = input("Nacionalidade: ")
        print(autor_service.cadastrar(nome, nacionalidade))
    elif op == "2":
        for a in autor_service.listar():
            print(a)
    elif op == "3":
        id = int(input("ID do autor: "))
        a = autor_service.buscar_por_id(id)
        if a:
            a.nome = input(f"Novo nome ({a.nome}): ") or a.nome
            autor_service.atualizar(a)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do autor: "))
        print("Excluído!" if autor_service.excluir(id) else "Não encontrado.")
    elif op == "5":
        termo = input("Nome (parcial): ")
        for a in autor_service.pesquisar_por_nome(termo):
            print(a)


def _menu_editoras(editora_service):
    print("\n-- Editoras --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir 5-Pesquisar por nome")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        cidade = input("Cidade: ")
        print(editora_service.cadastrar(nome, cidade))
    elif op == "2":
        for e in editora_service.listar():
            print(e)
    elif op == "3":
        id = int(input("ID da editora: "))
        e = editora_service.buscar_por_id(id)
        if e:
            e.nome = input(f"Novo nome ({e.nome}): ") or e.nome
            editora_service.atualizar(e)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID da editora: "))
        print("Excluído!" if editora_service.excluir(id) else "Não encontrado.")
    elif op == "5":
        termo = input("Nome (parcial): ")
        for e in editora_service.pesquisar_por_nome(termo):
            print(e)


def _menu_livros(livro_service):
    print("\n-- Livros --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        titulo = input("Título: ")
        isbn = input("ISBN: ")
        cat_id = int(input("ID da categoria: "))
        autor_id = int(input("ID do autor: "))
        editora_id = int(input("ID da editora: "))
        qtd = int(input("Quantidade de exemplares: "))
        try:
            print(livro_service.cadastrar(titulo, isbn, cat_id, autor_id, editora_id, qtd))
        except ValueError as e:
            print(f"Erro: {e}")
    elif op == "2":
        for l in livro_service.listar():
            print(l)
    elif op == "3":
        id = int(input("ID do livro: "))
        l = livro_service.buscar_por_id(id)
        if l:
            l.titulo = input(f"Novo título ({l.titulo}): ") or l.titulo
            livro_service.atualizar(l)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do livro: "))
        print("Excluído!" if livro_service.excluir(id) else "Não encontrado.")


def _menu_usuarios(usuario_service):
    print("\n-- Usuários --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir 5-Pesquisar por nome")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        perfil = input("Perfil (admin/leitor): ")
        try:
            print(usuario_service.cadastrar(nome, email, senha, perfil))
        except ValueError as e:
            print(f"Erro: {e}")
    elif op == "2":
        for u in usuario_service.listar():
            print(u)
    elif op == "3":
        id = int(input("ID do usuário: "))
        u = usuario_service.buscar_por_id(id)
        if u:
            u.nome = input(f"Novo nome ({u.nome}): ") or u.nome
            usuario_service.atualizar(u)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do usuário: "))
        print("Excluído!" if usuario_service.excluir(id) else "Não encontrado.")
    elif op == "5":
        termo = input("Nome (parcial): ")
        for u in usuario_service.pesquisar_por_nome(termo):
            print(u)


def _vincular_livro(livro_service):
    print("\n-- Vincular Livro --")
    print("1-Vincular a Categoria  2-Vincular a Autor  3-Vincular a Editora")
    op = input("Opção: ").strip()
    livro_id = int(input("ID do livro: "))
    try:
        if op == "1":
            categoria_id = int(input("ID da categoria: "))
            print(livro_service.vincular_categoria(livro_id, categoria_id))
        elif op == "2":
            autor_id = int(input("ID do autor: "))
            print(livro_service.vincular_autor(livro_id, autor_id))
        elif op == "3":
            editora_id = int(input("ID da editora: "))
            print(livro_service.vincular_editora(livro_id, editora_id))
    except ValueError as e:
        print(f"Erro: {e}")


def _pesquisar_livro(livro_service):
    termo = input("Título (parcial): ")
    for l in livro_service.pesquisar_por_titulo(termo):
        print(l)


def _registrar_devolucao(emprestimo_service):
    id = int(input("ID do empréstimo: "))
    try:
        print(emprestimo_service.registrar_devolucao(id))
    except ValueError as e:
        print(f"Erro: {e}")
