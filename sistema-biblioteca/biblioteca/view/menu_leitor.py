from service.livro_service import LivroService
from service.emprestimo_service import EmprestimoService


def menu_leitor(usuario_logado):
    livro_service = LivroService()
    emprestimo_service = EmprestimoService()

    while True:
        print(f"\n=== MENU LEITOR ({usuario_logado.nome}) ===")
        print("1 - Pesquisar Livro por título")
        print("2 - Realizar Empréstimo")
        print("3 - Meus Empréstimos")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            termo = input("Título (parcial): ")
            for l in livro_service.pesquisar_por_titulo(termo):
                print(l)
        elif opcao == "2":
            livro_id = int(input("ID do livro desejado: "))
            try:
                emp = emprestimo_service.realizar_emprestimo(livro_id, usuario_logado.id)
                print(f"Empréstimo realizado com sucesso! {emp}")
            except ValueError as e:
                print(f"Erro: {e}")
        elif opcao == "3":
            for e in emprestimo_service.listar_por_usuario(usuario_logado.id):
                print(e)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
