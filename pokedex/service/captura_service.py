from datetime import datetime

from model.captura import Captura
from persistence.captura_repositorio import CapturaRepositorio
from persistence.pokemon_repositorio import PokemonRepositorio
from persistence.usuario_repositorio import UsuarioRepositorio


class CapturaService:
    def __init__(self):
        self.repositorio = CapturaRepositorio()
        self.repositorio_pokemon = PokemonRepositorio()
        self.repositorio_usuario = UsuarioRepositorio()

    def capturar_pokemon(self, pokemon_id, treinador_id, apelido=""):
        """
        Regra de negócio que manipula mais de uma entidade em uma mesma operação:
        - valida o treinador e o pokémon
        - verifica se há pokémons disponíveis na natureza para captura
        - insere um novo registro em Captura
        - atualiza (decrementa) a quantidade disponível em Pokemon
        """
        pokemon = self.repositorio_pokemon.buscar_por_id(pokemon_id)
        if not pokemon:
            raise ValueError("Pokémon não encontrado.")

        treinador = self.repositorio_usuario.buscar_por_id(treinador_id)
        if not treinador:
            raise ValueError("Treinador não encontrado.")

        if pokemon.qtd_disponivel <= 0:
            raise ValueError(f"Não há '{pokemon.nome}' selvagens disponíveis para captura no momento.")

        data_captura = datetime.now().strftime("%Y-%m-%d")
        apelido_final = apelido if apelido else pokemon.nome

        captura = Captura(
            pokemon_id=pokemon_id,
            treinador_id=treinador_id,
            apelido=apelido_final,
            data_captura=data_captura,
        )
        captura = self.repositorio.inserir(captura)

        # Efeito colateral em outra entidade (Pokemon): baixa na quantidade disponível
        pokemon.qtd_disponivel -= 1
        self.repositorio_pokemon.atualizar(pokemon)

        return captura

    def libertar_pokemon(self, captura_id):
        """
        Regra de negócio que manipula mais de uma entidade em uma mesma operação:
        - atualiza a Captura (status e data de libertação)
        - atualiza o Pokemon (incrementa a quantidade disponível na natureza)
        """
        captura = self.repositorio.buscar_por_id(captura_id)
        if not captura:
            raise ValueError("Captura não encontrada.")

        if captura.status == Captura.STATUS_LIBERTADO:
            raise ValueError("Este Pokémon já foi libertado.")

        captura.status = Captura.STATUS_LIBERTADO
        captura.data_libertacao = datetime.now().strftime("%Y-%m-%d")
        self.repositorio.atualizar(captura)

        pokemon = self.repositorio_pokemon.buscar_por_id(captura.pokemon_id)
        if pokemon:
            pokemon.qtd_disponivel = min(pokemon.qtd_avistados, pokemon.qtd_disponivel + 1)
            self.repositorio_pokemon.atualizar(pokemon)

        return captura

    def listar(self):
        return self.repositorio.listar()

    def listar_por_treinador(self, treinador_id):
        return self.repositorio.listar_por_treinador(treinador_id)

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, captura):
        return self.repositorio.atualizar(captura)

    def excluir(self, id):
        return self.repositorio.excluir(id)
