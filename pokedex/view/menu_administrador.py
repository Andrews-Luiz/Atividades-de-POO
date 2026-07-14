from pokedex.service.tipo_service import TipoService
from pokedex.service.habitat_service import HabitatService
from pokedex.service.regiao_service import RegiaoService
from pokedex.service.pokemon_service import PokemonService
from pokedex.service.usuario_service import UsuarioService
from pokedex.service.captura_service import CapturaService


def menu_administrador(usuario_logado):
    tipo_service = TipoService()
    habitat_service = HabitatService()
    regiao_service = RegiaoService()
    pokemon_service = PokemonService()
    usuario_service = UsuarioService()
    captura_service = CapturaService()

    while True:
        print(f"\n=== MENU ADMINISTRADOR ({usuario_logado.nome}) ===")
        print("1 - Gerenciar Tipos")
        print("2 - Gerenciar Habitats")
        print("3 - Gerenciar Regiões")
        print("4 - Gerenciar Pokémons (Pokédex)")
        print("5 - Gerenciar Usuários")
        print("6 - Vincular Pokémon a Tipo / Habitat / Região")
        print("7 - Pesquisar Pokémon por nome")
        print("8 - Gerenciar Capturas (listar / atualizar apelido / excluir)")
        print("9 - Registrar Libertação de Pokémon (regra de negócio)")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            _menu_tipos(tipo_service)
        elif opcao == "2":
            _menu_habitats(habitat_service)
        elif opcao == "3":
            _menu_regioes(regiao_service)
        elif opcao == "4":
            _menu_pokemons(pokemon_service)
        elif opcao == "5":
            _menu_usuarios(usuario_service)
        elif opcao == "6":
            _vincular_pokemon(pokemon_service)
        elif opcao == "7":
            _pesquisar_pokemon(pokemon_service)
        elif opcao == "8":
            _menu_capturas(captura_service)
        elif opcao == "9":
            _libertar_pokemon(captura_service)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def _menu_tipos(tipo_service):
    print("\n-- Tipos --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome (ex: Fogo, Água, Grama): ")
        desc = input("Descrição: ")
        print(tipo_service.cadastrar(nome, desc))
    elif op == "2":
        for t in tipo_service.listar():
            print(t)
    elif op == "3":
        id = int(input("ID do tipo: "))
        t = tipo_service.buscar_por_id(id)
        if t:
            t.nome = input(f"Novo nome ({t.nome}): ") or t.nome
            tipo_service.atualizar(t)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do tipo: "))
        print("Excluído!" if tipo_service.excluir(id) else "Não encontrado.")


def _menu_habitats(habitat_service):
    print("\n-- Habitats --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome (ex: Floresta, Caverna, Oceano): ")
        desc = input("Descrição: ")
        print(habitat_service.cadastrar(nome, desc))
    elif op == "2":
        for h in habitat_service.listar():
            print(h)
    elif op == "3":
        id = int(input("ID do habitat: "))
        h = habitat_service.buscar_por_id(id)
        if h:
            h.nome = input(f"Novo nome ({h.nome}): ") or h.nome
            habitat_service.atualizar(h)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do habitat: "))
        print("Excluído!" if habitat_service.excluir(id) else "Não encontrado.")


def _menu_regioes(regiao_service):
    print("\n-- Regiões --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome (ex: Kanto, Johto): ")
        desc = input("Descrição: ")
        print(regiao_service.cadastrar(nome, desc))
    elif op == "2":
        for r in regiao_service.listar():
            print(r)
    elif op == "3":
        id = int(input("ID da região: "))
        r = regiao_service.buscar_por_id(id)
        if r:
            r.nome = input(f"Novo nome ({r.nome}): ") or r.nome
            regiao_service.atualizar(r)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID da região: "))
        print("Excluído!" if regiao_service.excluir(id) else "Não encontrado.")


def _menu_pokemons(pokemon_service):
    print("\n-- Pokémons --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        numero = int(input("Número na Pokédex: "))
        tipo_id = int(input("ID do tipo: "))
        habitat_id = int(input("ID do habitat: "))
        regiao_id = int(input("ID da região: "))
        hp_base = int(input("HP base: "))
        qtd = int(input("Quantidade avistada na natureza: "))
        try:
            print(pokemon_service.cadastrar(nome, numero, tipo_id, habitat_id, regiao_id, hp_base, qtd))
        except ValueError as e:
            print(f"Erro: {e}")
    elif op == "2":
        for p in pokemon_service.listar():
            print(p)
    elif op == "3":
        id = int(input("ID do pokémon: "))
        p = pokemon_service.buscar_por_id(id)
        if p:
            p.nome = input(f"Novo nome ({p.nome}): ") or p.nome
            pokemon_service.atualizar(p)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do pokémon: "))
        print("Excluído!" if pokemon_service.excluir(id) else "Não encontrado.")


def _menu_usuarios(usuario_service):
    print("\n-- Usuários --")
    print("1-Inserir 2-Listar 3-Atualizar 4-Excluir 5-Pesquisar por nome")
    op = input("Opção: ").strip()
    if op == "1":
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        perfil = input("Perfil (admin/treinador): ")
        try:
            print(usuario_service.cadastrar(nome, email, senha, perfil))
        except ValueError as e:
            print(f"Erro: {e}")
    elif op == "2":
        for u in usuario_service.listar():
            print(u)
    elif op == "3":
        id = int(input("ID do usuário: "))
        u = usuario_service.buscar_por_id(id)
        if u:
            u.nome = input(f"Novo nome ({u.nome}): ") or u.nome
            usuario_service.atualizar(u)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "4":
        id = int(input("ID do usuário: "))
        print("Excluído!" if usuario_service.excluir(id) else "Não encontrado.")
    elif op == "5":
        termo = input("Nome (parcial): ")
        for u in usuario_service.pesquisar_por_nome(termo):
            print(u)


def _vincular_pokemon(pokemon_service):
    print("\n-- Vincular Pokémon --")
    print("1-Vincular a Tipo  2-Vincular a Habitat  3-Vincular a Região")
    op = input("Opção: ").strip()
    pokemon_id = int(input("ID do pokémon: "))
    try:
        if op == "1":
            tipo_id = int(input("ID do tipo: "))
            print(pokemon_service.vincular_tipo(pokemon_id, tipo_id))
        elif op == "2":
            habitat_id = int(input("ID do habitat: "))
            print(pokemon_service.vincular_habitat(pokemon_id, habitat_id))
        elif op == "3":
            regiao_id = int(input("ID da região: "))
            print(pokemon_service.vincular_regiao(pokemon_id, regiao_id))
    except ValueError as e:
        print(f"Erro: {e}")


def _pesquisar_pokemon(pokemon_service):
    termo = input("Nome (parcial): ")
    for p in pokemon_service.pesquisar_por_nome(termo):
        print(p)


def _menu_capturas(captura_service):
    print("\n-- Capturas --")
    print("1-Listar todas 2-Atualizar apelido 3-Excluir 4-Listar por treinador")
    op = input("Opção: ").strip()
    if op == "1":
        for c in captura_service.listar():
            print(c)
    elif op == "2":
        id = int(input("ID da captura: "))
        c = captura_service.buscar_por_id(id)
        if c:
            c.apelido = input(f"Novo apelido ({c.apelido}): ") or c.apelido
            captura_service.atualizar(c)
            print("Atualizado!")
        else:
            print("Não encontrado.")
    elif op == "3":
        id = int(input("ID da captura: "))
        print("Excluído!" if captura_service.excluir(id) else "Não encontrado.")
    elif op == "4":
        treinador_id = int(input("ID do treinador: "))
        for c in captura_service.listar_por_treinador(treinador_id):
            print(c)


def _libertar_pokemon(captura_service):
    id = int(input("ID da captura: "))
    try:
        print(captura_service.libertar_pokemon(id))
    except ValueError as e:
        print(f"Erro: {e}")
