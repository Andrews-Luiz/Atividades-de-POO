from model.editora import Editora
from persistence.repositorio_base import RepositorioBase


class EditoraRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("editoras.json", Editora, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [e for e in self.carregar_todos() if termo in e.nome.lower()]
