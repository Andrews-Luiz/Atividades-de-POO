from model.categoria import Categoria
from persistence.repositorio_base import RepositorioBase


class CategoriaRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("categorias.json", Categoria, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [c for c in self.carregar_todos() if termo in c.nome.lower()]
