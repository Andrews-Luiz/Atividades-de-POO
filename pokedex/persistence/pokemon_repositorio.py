from pokedex.model.pokemon import Pokemon
from pokedex.persistence.repositorio_base import RepositorioBase


class PokemonRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("pokemons.json", Pokemon, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [p for p in self.carregar_todos() if termo in p.nome.lower()]

    def listar_por_tipo(self, tipo_id):
        return [p for p in self.carregar_todos() if p.tipo_id == tipo_id]
