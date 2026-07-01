from datetime import datetime, timedelta

from model.emprestimo import Emprestimo
from persistence.emprestimo_repositorio import EmprestimoRepositorio
from persistence.livro_repositorio import LivroRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio

DIAS_PRAZO_PADRAO = 7


class EmprestimoService:
    def __init__(self):
        self.repositorio = EmprestimoRepositorio()
        self.repositorio_livro = LivroRepositorio()
        self.repositorio_usuario = UsuarioRepositorio()

    def realizar_emprestimo(self, livro_id, usuario_id, dias_prazo=DIAS_PRAZO_PADRAO):
        """
        Regra de negócio que manipula mais de uma entidade em uma mesma operação:
        - valida o usuário e o livro
        - verifica disponibilidade de exemplares
        - insere um novo registro em Emprestimo
        - atualiza (decrementa) a quantidade disponível em Livro
        """
        livro = self.repositorio_livro.buscar_por_id(livro_id)
        if not livro:
            raise ValueError("Livro não encontrado.")

        usuario = self.repositorio_usuario.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if livro.qtd_disponivel <= 0:
            raise ValueError(f"Não há exemplares disponíveis do livro '{livro.titulo}'.")

        hoje = datetime.now()
        data_emprestimo = hoje.strftime("%Y-%m-%d")
        data_devolucao_prevista = (hoje + timedelta(days=dias_prazo)).strftime("%Y-%m-%d")

        emprestimo = Emprestimo(
            livro_id=livro_id,
            usuario_id=usuario_id,
            data_emprestimo=data_emprestimo,
            data_devolucao_prevista=data_devolucao_prevista,
        )
        emprestimo = self.repositorio.inserir(emprestimo)

        # Efeito colateral em outra entidade (Livro): baixa no estoque disponível
        livro.qtd_disponivel -= 1
        self.repositorio_livro.atualizar(livro)

        return emprestimo

    def registrar_devolucao(self, emprestimo_id):
        """
        Regra de negócio que manipula mais de uma entidade em uma mesma operação:
        - atualiza o Emprestimo (status e data de devolução real)
        - atualiza o Livro (incrementa a quantidade disponível)
        """
        emprestimo = self.repositorio.buscar_por_id(emprestimo_id)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")

        if emprestimo.status == Emprestimo.STATUS_DEVOLVIDO:
            raise ValueError("Este empréstimo já foi devolvido.")

        emprestimo.status = Emprestimo.STATUS_DEVOLVIDO
        emprestimo.data_devolucao_real = datetime.now().strftime("%Y-%m-%d")
        self.repositorio.atualizar(emprestimo)

        livro = self.repositorio_livro.buscar_por_id(emprestimo.livro_id)
        if livro:
            livro.qtd_disponivel = min(livro.qtd_total, livro.qtd_disponivel + 1)
            self.repositorio_livro.atualizar(livro)

        return emprestimo

    def listar(self):
        return self.repositorio.listar()

    def listar_por_usuario(self, usuario_id):
        return self.repositorio.listar_por_usuario(usuario_id)

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def excluir(self, id):
        return self.repositorio.excluir(id)
