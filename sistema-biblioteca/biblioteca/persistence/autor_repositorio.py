from model.autor import Autor
from persistence.repositorio_base import RepositorioBase


class AutorRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("autores.json", Autor, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [a for a in self.carregar_todos() if termo in a.nome.lower()]
