from pokedex.model.regiao import Regiao
from pokedex.persistence.repositorio_base import RepositorioBase


class RegiaoRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("regioes.json", Regiao, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [r for r in self.carregar_todos() if termo in r.nome.lower()]
