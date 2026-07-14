from pokedex.model.tipo import Tipo
from pokedex.persistence.repositorio_base import RepositorioBase


class TipoRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("tipos.json", Tipo, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [t for t in self.carregar_todos() if termo in t.nome.lower()]
