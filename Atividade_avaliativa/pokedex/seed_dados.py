"""
Script para popular o sistema com dados de exemplo (opcional).
Cria um admin, um treinador, tipos, habitats, regiões e pokémons para
testar o sistema via main.py sem precisar cadastrar tudo manualmente.

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
tipo_fogo = tipo_service.cadastrar("Fogo", "Forte contra Grama, fraco contra Água")
tipo_agua = tipo_service.cadastrar("Água", "Forte contra Fogo, fraco contra Elétrico")
tipo_grama = tipo_service.cadastrar("Grama", "Forte contra Água, fraco contra Fogo")
tipo_eletrico = tipo_service.cadastrar("Elétrico", "Forte contra Água, fraco contra Terra")

print("Criando habitats de exemplo...")
habitat_floresta = habitat_service.cadastrar("Floresta", "Áreas com muita vegetação")
habitat_montanha = habitat_service.cadastrar("Montanha", "Regiões rochosas e elevadas")
habitat_oceano = habitat_service.cadastrar("Oceano", "Áreas aquáticas profundas")

print("Criando regiões de exemplo...")
regiao_kanto = regiao_service.cadastrar("Kanto", "Primeira região explorada pelos treinadores")
regiao_johto = regiao_service.cadastrar("Johto", "Região vizinha a Kanto")

print("Criando pokémons de exemplo...")
pokemon_service.cadastrar("Pikachu", 25, tipo_eletrico.id, habitat_floresta.id, regiao_kanto.id, hp_base=35, qtd_avistados=5)
pokemon_service.cadastrar("Charmander", 4, tipo_fogo.id, habitat_montanha.id, regiao_kanto.id, hp_base=39, qtd_avistados=3)
pokemon_service.cadastrar("Squirtle", 7, tipo_agua.id, habitat_oceano.id, regiao_kanto.id, hp_base=44, qtd_avistados=3)
pokemon_service.cadastrar("Bulbasaur", 1, tipo_grama.id, habitat_floresta.id, regiao_kanto.id, hp_base=45, qtd_avistados=4)

print("\nDados de exemplo criados com sucesso!")
print("Login admin -> email: admin@pokemanager.com     | senha: admin123")
print("Login treinador -> email: ash@pokemanager.com    | senha: treinador123")
