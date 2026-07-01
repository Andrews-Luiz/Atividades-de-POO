from model.emprestimo import Emprestimo
from persistence.repositorio_base import RepositorioBase


class EmprestimoRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("emprestimos.json", Emprestimo, pasta_dados)

    def listar_por_usuario(self, usuario_id):
        return [e for e in self.carregar_todos() if e.usuario_id == usuario_id]

    def listar_ativos_por_livro(self, livro_id):
        return [e for e in self.carregar_todos()
                if e.livro_id == livro_id and e.status == Emprestimo.STATUS_ATIVO]
