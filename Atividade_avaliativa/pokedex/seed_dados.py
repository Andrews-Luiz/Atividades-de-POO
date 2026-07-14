"""
Script para popular o sistema com dados de exemplo (opcional).
Cria um admin, um treinador, tipos, habitats, regiões e 10 pokémons da
primeira geração (Kanto) para testar o sistema via main.py sem precisar
cadastrar tudo manualmente.

O script é idempotente: pode ser executado várias vezes sem duplicar
registros, pois verifica se cada item já existe (por nome/e-mail) antes
de cadastrar.

Execução: python3 seed_dados.py
"""
from service.usuario_service import UsuarioService
from service.tipo_service import TipoService
from service.habitat_service import HabitatService
from service.regiao_service import RegiaoService
from service.pokemon_service import PokemonService
from model.usuario import Usuario

usuario_service = UsuarioService()
tipo_service = TipoService()
habitat_service = HabitatService()
regiao_service = RegiaoService()
pokemon_service = PokemonService()


def obter_ou_criar_tipo(nome, descricao):
    for t in tipo_service.listar():
        if t.nome.lower() == nome.lower():
            return t
    return tipo_service.cadastrar(nome, descricao)


def obter_ou_criar_habitat(nome, descricao):
    for h in habitat_service.listar():
        if h.nome.lower() == nome.lower():
            return h
    return habitat_service.cadastrar(nome, descricao)


def obter_ou_criar_regiao(nome, descricao):
    for r in regiao_service.listar():
        if r.nome.lower() == nome.lower():
            return r
    return regiao_service.cadastrar(nome, descricao)


def obter_ou_criar_pokemon(nome, numero, tipo_id, habitat_id, regiao_id, hp_base, qtd_avistados):
    for p in pokemon_service.listar():
        if p.nome.lower() == nome.lower():
            return p
    return pokemon_service.cadastrar(nome, numero, tipo_id, habitat_id, regiao_id, hp_base, qtd_avistados)


print("Criando usuários de exemplo...")
try:
    usuario_service.cadastrar("Admin Geral", "admin@pokemanager.com", "admin123", Usuario.PERFIL_ADMIN)
except ValueError as e:
    print(f"  (aviso) {e}")
try:
    usuario_service.cadastrar("Ash Treinador", "ash@pokemanager.com", "treinador123", Usuario.PERFIL_TREINADOR)
except ValueError as e:
    print(f"  (aviso) {e}")

print("Criando tipos de exemplo...")
tipo_grama = obter_ou_criar_tipo("Grama", "Forte contra Água, fraco contra Fogo")
tipo_fogo = obter_ou_criar_tipo("Fogo", "Forte contra Grama, fraco contra Água")
tipo_agua = obter_ou_criar_tipo("Água", "Forte contra Fogo, fraco contra Elétrico")
tipo_eletrico = obter_ou_criar_tipo("Elétrico", "Forte contra Água, fraco contra Terra")
tipo_normal = obter_ou_criar_tipo("Normal", "Não possui vantagens ou fraquezas de tipo marcantes")
tipo_psiquico = obter_ou_criar_tipo("Psíquico", "Forte contra Lutador e Venenoso")
tipo_fantasma = obter_ou_criar_tipo("Fantasma", "Forte contra Psíquico, imune a golpes Normais")

print("Criando habitats de exemplo...")
habitat_floresta = obter_ou_criar_habitat("Floresta", "Áreas com muita vegetação")
habitat_montanha = obter_ou_criar_habitat("Montanha", "Regiões rochosas e elevadas")
habitat_oceano = obter_ou_criar_habitat("Oceano", "Áreas aquáticas profundas")
habitat_urbano = obter_ou_criar_habitat("Urbano", "Cidades e vilarejos")
habitat_caverna = obter_ou_criar_habitat("Caverna", "Ambientes escuros e subterrâneos")

print("Criando regiões de exemplo...")
regiao_kanto = obter_ou_criar_regiao("Kanto", "Primeira região explorada pelos treinadores")
regiao_johto = obter_ou_criar_regiao("Johto", "Região vizinha a Kanto")

print("Criando 10 pokémons da primeira geração (Kanto)...")
obter_ou_criar_pokemon("Bulbasaur", 1, tipo_grama.id, habitat_floresta.id, regiao_kanto.id, hp_base=45, qtd_avistados=4)
obter_ou_criar_pokemon("Charmander", 4, tipo_fogo.id, habitat_montanha.id, regiao_kanto.id, hp_base=39, qtd_avistados=3)
obter_ou_criar_pokemon("Squirtle", 7, tipo_agua.id, habitat_oceano.id, regiao_kanto.id, hp_base=44, qtd_avistados=3)
obter_ou_criar_pokemon("Pikachu", 25, tipo_eletrico.id, habitat_floresta.id, regiao_kanto.id, hp_base=35, qtd_avistados=5)
obter_ou_criar_pokemon("Jigglypuff", 39, tipo_normal.id, habitat_floresta.id, regiao_kanto.id, hp_base=115, qtd_avistados=4)
obter_ou_criar_pokemon("Meowth", 52, tipo_normal.id, habitat_urbano.id, regiao_kanto.id, hp_base=40, qtd_avistados=6)
obter_ou_criar_pokemon("Psyduck", 54, tipo_agua.id, habitat_oceano.id, regiao_kanto.id, hp_base=50, qtd_avistados=4)
obter_ou_criar_pokemon("Growlithe", 58, tipo_fogo.id, habitat_montanha.id, regiao_kanto.id, hp_base=55, qtd_avistados=2)
obter_ou_criar_pokemon("Abra", 63, tipo_psiquico.id, habitat_urbano.id, regiao_kanto.id, hp_base=25, qtd_avistados=3)
obter_ou_criar_pokemon("Gastly", 92, tipo_fantasma.id, habitat_caverna.id, regiao_kanto.id, hp_base=30, qtd_avistados=2)

print("\nDados de exemplo criados com sucesso!")
print("Login admin -> email: admin@pokemanager.com     | senha: admin123")
print("Login treinador -> email: ash@pokemanager.com    | senha: treinador123")
