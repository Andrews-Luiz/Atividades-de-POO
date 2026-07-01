from model.habitat import Habitat
from persistence.repositorio_base import RepositorioBase


class HabitatRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("habitats.json", Habitat, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [h for h in self.carregar_todos() if termo in h.nome.lower()]
