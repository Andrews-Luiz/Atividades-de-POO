from model.livro import Livro
from persistence.repositorio_base import RepositorioBase


class LivroRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("livros.json", Livro, pasta_dados)

    def pesquisar_por_titulo(self, termo):
        termo = termo.lower()
        return [l for l in self.carregar_todos() if termo in l.titulo.lower()]

    def listar_por_categoria(self, categoria_id):
        return [l for l in self.carregar_todos() if l.categoria_id == categoria_id]
