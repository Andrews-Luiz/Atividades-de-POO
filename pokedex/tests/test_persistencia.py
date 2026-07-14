"""
Testes de persistência: verificam se é possível salvar e ler
objetos das classes do modelo em arquivo JSON, além de validar
uma regra de negócio que envolve mais de uma entidade.

Execução: python3 -m unittest tests.test_persistencia -v
(a partir da raiz do projeto)
"""
import os
import shutil
import unittest

from pokedex.model.usuario import Usuario
from pokedex.model.tipo import Tipo
from pokedex.model.habitat import Habitat
from pokedex.model.regiao import Regiao
from pokedex.model.pokemon import Pokemon
from pokedex.model.captura import Captura

from pokedex.persistence.usuario_repositorio import UsuarioRepositorio
from pokedex.persistence.tipo_repositorio import TipoRepositorio
from pokedex.persistence.habitat_repositorio import HabitatRepositorio
from pokedex.persistence.regiao_repositorio import RegiaoRepositorio
from pokedex.persistence.pokemon_repositorio import PokemonRepositorio
from pokedex.persistence.captura_repositorio import CapturaRepositorio

from pokedex.service.captura_service import CapturaService
from pokedex.service.pokemon_service import PokemonService
from pokedex.service.usuario_service import UsuarioService
from pokedex.service.tipo_service import TipoService
from pokedex.service.habitat_service import HabitatService
from pokedex.service.regiao_service import RegiaoService

PASTA_TESTE = "data_teste"


class TestPersistenciaUsuario(unittest.TestCase):
    def setUp(self):
        self.repo = UsuarioRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_usuario(self):
        usuario = Usuario(nome="Ana Souza", email="ana@email.com",
                           senha="123456", perfil=Usuario.PERFIL_TREINADOR)
        usuario_salvo = self.repo.inserir(usuario)
        self.assertIsNotNone(usuario_salvo.id)

        # Simula reabertura do sistema: cria um novo repositório e lê do arquivo
        repo2 = UsuarioRepositorio(pasta_dados=PASTA_TESTE)
        usuarios = repo2.listar()

        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nome, "Ana Souza")
        self.assertEqual(usuarios[0].email, "ana@email.com")
        self.assertEqual(usuarios[0].perfil, Usuario.PERFIL_TREINADOR)


class TestPersistenciaTipo(unittest.TestCase):
    def setUp(self):
        self.repo = TipoRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_tipo(self):
        tipo = Tipo(nome="Fogo", descricao="Forte contra Grama")
        self.repo.inserir(tipo)

        repo2 = TipoRepositorio(pasta_dados=PASTA_TESTE)
        tipos = repo2.listar()

        self.assertEqual(len(tipos), 1)
        self.assertEqual(tipos[0].nome, "Fogo")


class TestPersistenciaHabitat(unittest.TestCase):
    def setUp(self):
        self.repo = HabitatRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_habitat(self):
        habitat = Habitat(nome="Floresta", descricao="Área com muita vegetação")
        self.repo.inserir(habitat)

        repo2 = HabitatRepositorio(pasta_dados=PASTA_TESTE)
        habitats = repo2.listar()

        self.assertEqual(len(habitats), 1)
        self.assertEqual(habitats[0].nome, "Floresta")


class TestPersistenciaRegiao(unittest.TestCase):
    def setUp(self):
        self.repo = RegiaoRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_regiao(self):
        regiao = Regiao(nome="Kanto", descricao="Primeira região")
        self.repo.inserir(regiao)

        repo2 = RegiaoRepositorio(pasta_dados=PASTA_TESTE)
        regioes = repo2.listar()

        self.assertEqual(len(regioes), 1)
        self.assertEqual(regioes[0].nome, "Kanto")


class TestPersistenciaPokemon(unittest.TestCase):
    def setUp(self):
        self.repo = PokemonRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_pokemon(self):
        pokemon = Pokemon(nome="Pikachu", numero_pokedex=25, tipo_id=1,
                           habitat_id=1, regiao_id=1, hp_base=35, qtd_avistados=5)
        self.repo.inserir(pokemon)

        repo2 = PokemonRepositorio(pasta_dados=PASTA_TESTE)
        pokemons = repo2.listar()

        self.assertEqual(len(pokemons), 1)
        self.assertEqual(pokemons[0].nome, "Pikachu")
        self.assertEqual(pokemons[0].qtd_disponivel, 5)  # criado igual à qtd_avistados

    def test_atualizar_e_excluir_pokemon(self):
        pokemon = self.repo.inserir(Pokemon(nome="Charmander", numero_pokedex=4, tipo_id=1,
                                             habitat_id=1, regiao_id=1, hp_base=39, qtd_avistados=2))
        pokemon.qtd_disponivel = 1
        self.assertTrue(self.repo.atualizar(pokemon))

        recarregado = self.repo.buscar_por_id(pokemon.id)
        self.assertEqual(recarregado.qtd_disponivel, 1)

        self.assertTrue(self.repo.excluir(pokemon.id))
        self.assertIsNone(self.repo.buscar_por_id(pokemon.id))


class TestPersistenciaCaptura(unittest.TestCase):
    def setUp(self):
        self.repo = CapturaRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_captura(self):
        captura = Captura(pokemon_id=1, treinador_id=1, apelido="Pika",
                           data_captura="2026-07-01")
        self.repo.inserir(captura)

        repo2 = CapturaRepositorio(pasta_dados=PASTA_TESTE)
        capturas = repo2.listar()

        self.assertEqual(len(capturas), 1)
        self.assertEqual(capturas[0].status, Captura.STATUS_ATIVO)

    def test_atualizar_e_excluir_captura(self):
        captura = self.repo.inserir(Captura(pokemon_id=1, treinador_id=1, apelido="Pika",
                                             data_captura="2026-07-01"))
        captura.apelido = "PikaBolt"
        self.assertTrue(self.repo.atualizar(captura))

        recarregada = self.repo.buscar_por_id(captura.id)
        self.assertEqual(recarregada.apelido, "PikaBolt")

        self.assertTrue(self.repo.excluir(captura.id))
        self.assertIsNone(self.repo.buscar_por_id(captura.id))


class TestRegraDeNegocioCaptura(unittest.TestCase):
    """
    Testa a regra de negócio que manipula objetos de mais de uma entidade
    em uma mesma operação: ao capturar um Pokémon, o sistema insere um
    registro em Captura e atualiza a quantidade disponível em Pokemon.
    O mesmo vale para a libertação (operação inversa).
    """

    def setUp(self):
        os.makedirs(PASTA_TESTE, exist_ok=True)

        self.usuario_service = UsuarioService()
        self.usuario_service.repositorio = UsuarioRepositorio(pasta_dados=PASTA_TESTE)

        self.tipo_service = TipoService()
        self.tipo_service.repositorio = TipoRepositorio(pasta_dados=PASTA_TESTE)

        self.habitat_service = HabitatService()
        self.habitat_service.repositorio = HabitatRepositorio(pasta_dados=PASTA_TESTE)

        self.regiao_service = RegiaoService()
        self.regiao_service.repositorio = RegiaoRepositorio(pasta_dados=PASTA_TESTE)

        self.pokemon_service = PokemonService()
        self.pokemon_service.repositorio = PokemonRepositorio(pasta_dados=PASTA_TESTE)
        self.pokemon_service.repositorio_tipo = self.tipo_service.repositorio
        self.pokemon_service.repositorio_habitat = self.habitat_service.repositorio
        self.pokemon_service.repositorio_regiao = self.regiao_service.repositorio

        self.captura_service = CapturaService()
        self.captura_service.repositorio = CapturaRepositorio(pasta_dados=PASTA_TESTE)
        self.captura_service.repositorio_pokemon = self.pokemon_service.repositorio
        self.captura_service.repositorio_usuario = self.usuario_service.repositorio

        self.tipo = self.tipo_service.cadastrar("Elétrico", "Forte contra Água")
        self.habitat = self.habitat_service.cadastrar("Floresta", "Área com vegetação")
        self.regiao = self.regiao_service.cadastrar("Kanto", "Primeira região")
        self.treinador = self.usuario_service.cadastrar(
            "Carlos Lima", "carlos@email.com", "senha123", Usuario.PERFIL_TREINADOR)
        self.pokemon = self.pokemon_service.cadastrar(
            "Pikachu", 25, self.tipo.id, self.habitat.id, self.regiao.id, hp_base=35, qtd_avistados=1)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_captura_diminui_disponibilidade_do_pokemon(self):
        self.assertEqual(self.pokemon.qtd_disponivel, 1)

        self.captura_service.capturar_pokemon(self.pokemon.id, self.treinador.id, "Pika")

        pokemon_atualizado = self.pokemon_service.buscar_por_id(self.pokemon.id)
        self.assertEqual(pokemon_atualizado.qtd_disponivel, 0)

    def test_nao_permite_captura_sem_pokemon_disponivel(self):
        self.captura_service.capturar_pokemon(self.pokemon.id, self.treinador.id)
        with self.assertRaises(ValueError):
            self.captura_service.capturar_pokemon(self.pokemon.id, self.treinador.id)

    def test_libertacao_restaura_disponibilidade_do_pokemon(self):
        captura = self.captura_service.capturar_pokemon(self.pokemon.id, self.treinador.id, "Pika")
        self.captura_service.libertar_pokemon(captura.id)

        pokemon_atualizado = self.pokemon_service.buscar_por_id(self.pokemon.id)
        self.assertEqual(pokemon_atualizado.qtd_disponivel, 1)

        captura_atualizada = self.captura_service.buscar_por_id(captura.id)
        self.assertEqual(captura_atualizada.status, Captura.STATUS_LIBERTADO)
        self.assertIsNotNone(captura_atualizada.data_libertacao)

    def test_vincular_pokemon_a_outro_tipo(self):
        novo_tipo = self.tipo_service.cadastrar("Psíquico", "Forte contra Lutador")
        pokemon_atualizado = self.pokemon_service.vincular_tipo(self.pokemon.id, novo_tipo.id)
        self.assertEqual(pokemon_atualizado.tipo_id, novo_tipo.id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
