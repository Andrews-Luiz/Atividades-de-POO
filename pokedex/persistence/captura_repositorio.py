from pokedex.model.captura import Captura
from pokedex.persistence.repositorio_base import RepositorioBase


class CapturaRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("capturas.json", Captura, pasta_dados)

    def listar_por_treinador(self, treinador_id):
        return [c for c in self.carregar_todos() if c.treinador_id == treinador_id]

    def listar_ativas_por_pokemon(self, pokemon_id):
        return [c for c in self.carregar_todos()
                if c.pokemon_id == pokemon_id and c.status == Captura.STATUS_ATIVO]
