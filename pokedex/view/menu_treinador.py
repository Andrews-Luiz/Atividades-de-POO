from pokedex.service.pokemon_service import PokemonService
from pokedex.service.captura_service import CapturaService


def menu_treinador(usuario_logado):
    pokemon_service = PokemonService()
    captura_service = CapturaService()

    while True:
        print(f"\n=== MENU TREINADOR ({usuario_logado.nome}) ===")
        print("1 - Pesquisar Pokémon por nome")
        print("2 - Capturar Pokémon")
        print("3 - Minha Equipe (minhas capturas)")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            termo = input("Nome (parcial): ")
            for p in pokemon_service.pesquisar_por_nome(termo):
                print(p)
        elif opcao == "2":
            pokemon_id = int(input("ID do pokémon desejado: "))
            apelido = input("Apelido (opcional, Enter para usar o nome padrão): ")
            try:
                captura = captura_service.capturar_pokemon(pokemon_id, usuario_logado.id, apelido)
                print(f"Pokémon capturado com sucesso! {captura}")
            except ValueError as e:
                print(f"Erro: {e}")
        elif opcao == "3":
            for c in captura_service.listar_por_treinador(usuario_logado.id):
                print(c)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
