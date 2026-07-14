from model.pokemon import Pokemon
from persistence.pokemon_repositorio import PokemonRepositorio
from persistence.tipo_repositorio import TipoRepositorio
from persistence.habitat_repositorio import HabitatRepositorio
from persistence.regiao_repositorio import RegiaoRepositorio


class PokemonService:
    def __init__(self):
        self.repositorio = PokemonRepositorio()
        self.repositorio_tipo = TipoRepositorio()
        self.repositorio_habitat = HabitatRepositorio()
        self.repositorio_regiao = RegiaoRepositorio()

    def cadastrar(self, nome, numero_pokedex, tipo_id, habitat_id, regiao_id,
                   hp_base, qtd_avistados):
        # Operações de associação: valida se tipo, habitat e regiao existem antes de vincular
        if tipo_id is not None and not self.repositorio_tipo.buscar_por_id(tipo_id):
            raise ValueError("Tipo informado não existe.")
        if habitat_id is not None and not self.repositorio_habitat.buscar_por_id(habitat_id):
            raise ValueError("Habitat informado não existe.")
        if regiao_id is not None and not self.repositorio_regiao.buscar_por_id(regiao_id):
            raise ValueError("Região informada não existe.")

        pokemon = Pokemon(nome=nome, numero_pokedex=numero_pokedex, tipo_id=tipo_id,
                           habitat_id=habitat_id, regiao_id=regiao_id, hp_base=hp_base,
                           qtd_avistados=qtd_avistados)
        return self.repositorio.inserir(pokemon)

    def vincular_tipo(self, pokemon_id, tipo_id):
        """Operação de associação: vincula um pokémon já existente a um tipo."""
        pokemon = self._buscar_pokemon_existente(pokemon_id)
        if not self.repositorio_tipo.buscar_por_id(tipo_id):
            raise ValueError("Tipo não encontrado.")
        pokemon.tipo_id = tipo_id
        self.repositorio.atualizar(pokemon)
        return pokemon

    def vincular_habitat(self, pokemon_id, habitat_id):
        """Operação de associação: vincula um pokémon já existente a um habitat."""
        pokemon = self._buscar_pokemon_existente(pokemon_id)
        if not self.repositorio_habitat.buscar_por_id(habitat_id):
            raise ValueError("Habitat não encontrado.")
        pokemon.habitat_id = habitat_id
        self.repositorio.atualizar(pokemon)
        return pokemon

    def vincular_regiao(self, pokemon_id, regiao_id):
        """Operação de associação: vincula um pokémon já existente a uma região."""
        pokemon = self._buscar_pokemon_existente(pokemon_id)
        if not self.repositorio_regiao.buscar_por_id(regiao_id):
            raise ValueError("Região não encontrada.")
        pokemon.regiao_id = regiao_id
        self.repositorio.atualizar(pokemon)
        return pokemon

    def _buscar_pokemon_existente(self, pokemon_id):
        pokemon = self.repositorio.buscar_por_id(pokemon_id)
        if not pokemon:
            raise ValueError("Pokémon não encontrado.")
        return pokemon

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, pokemon):
        return self.repositorio.atualizar(pokemon)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
