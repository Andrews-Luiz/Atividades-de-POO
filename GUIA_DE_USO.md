# Mini Guia de Uso — Sistema de Gerenciamento Pokémon

Este guia mostra, na prática, algumas das principais funções do sistema — tanto do
lado do **Treinador** quanto do **Administrador** — com exemplos reais de execução
no terminal.

---

## 0. Preparando o ambiente

Antes de tudo, popule o sistema com dados de exemplo (10 Pokémon da primeira
geração, tipos, habitats, regiões e dois usuários já cadastrados):

```
$ python3 seed_dados.py

Criando usuários de exemplo...
Criando tipos de exemplo...
Criando habitats de exemplo...
Criando regiões de exemplo...
Criando 10 pokémons da primeira geração (Kanto)...

Dados de exemplo criados com sucesso!
Login admin -> email: admin@pokemanager.com     | senha: admin123
Login treinador -> email: ash@pokemanager.com    | senha: treinador123
```

Esse script pode ser executado quantas vezes quiser: ele verifica se cada registro
já existe antes de criar, então **não duplica** dados em execuções repetidas.

Para iniciar o sistema:

```
$ python3 main.py
```

---

## Funções do perfil Treinador

### 1. Pesquisar um Pokémon pelo nome (parcial)

Login como treinador e busca parcial por "char":

```
E-mail: ash@pokemanager.com
Senha: treinador123

Bem-vindo(a), Ash Treinador! Perfil: treinador

=== MENU TREINADOR (Ash Treinador) ===
1 - Pesquisar Pokémon por nome
2 - Capturar Pokémon
3 - Minha Equipe (minhas capturas)
0 - Sair
Escolha uma opção: 1
Nome (parcial): char

Pokemon(id=2, nome='Charmander', disponivel=3/3)
```

A busca não diferencia maiúsculas/minúsculas e retorna qualquer Pokémon cujo nome
contenha o termo digitado.

### 2. Capturar um Pokémon (regra de negócio)

O treinador captura o Charmander (id=2) e dá um apelido a ele:

```
Escolha uma opção: 2
ID do pokémon desejado: 2
Apelido (opcional, Enter para usar o nome padrão): Charzinho

Pokémon capturado com sucesso! Captura(id=1, pokemon_id=2, treinador_id=2, apelido='Charzinho', status='ATIVO')
```

Por trás dos panos, essa única operação faz **duas coisas ao mesmo tempo**:
1. insere um novo registro em `Captura` (status `ATIVO`);
2. decrementa `qtd_disponivel` do Pokémon (de 3 para 2 exemplares selvagens).

Se não houvesse mais exemplares disponíveis, o sistema recusaria a captura:

```
Escolha uma opção: 2
ID do pokémon desejado: 2
Apelido (opcional, Enter para usar o nome padrão):
Erro: Não há 'Charmander' selvagens disponíveis para captura no momento.
```

### 3. Ver "Minha Equipe" (capturas do treinador logado)

```
Escolha uma opção: 3

Captura(id=1, pokemon_id=2, treinador_id=2, apelido='Charzinho', status='ATIVO')
```

Cada treinador só enxerga as próprias capturas — a consulta é filtrada pelo
`id` do usuário logado.

---

## Funções do perfil Administrador

### 4. Cadastrar um novo Tipo

```
E-mail: admin@pokemanager.com
Senha: admin123

Bem-vindo(a), Admin Geral! Perfil: admin

=== MENU ADMINISTRADOR (Admin Geral) ===
1 - Gerenciar Tipos
2 - Gerenciar Habitats
3 - Gerenciar Regiões
4 - Gerenciar Pokémons (Pokédex)
5 - Gerenciar Usuários
6 - Vincular Pokémon a Tipo / Habitat / Região
7 - Pesquisar Pokémon por nome
8 - Listar todas as Capturas
9 - Registrar Libertação de Pokémon
0 - Sair
Escolha uma opção: 1

-- Tipos --
1-Inserir 2-Listar 3-Atualizar 4-Excluir
Opção: 1
Nome (ex: Fogo, Água, Grama): Gelo
Descrição: Forte contra Voador, fraco contra Fogo

Tipo(id=8, nome='Gelo')
```

### 5. Cadastrar um novo Pokémon (associação com Tipo, Habitat e Região)

Cadastro do Articuno, já vinculando aos ids de Tipo, Habitat e Região existentes:

```
Escolha uma opção: 4

-- Pokémons --
1-Inserir 2-Listar 3-Atualizar 4-Excluir
Opção: 1
Nome: Articuno
Número na Pokédex: 144
ID do tipo: 8
ID do habitat: 2
ID da região: 1
HP base: 90
Quantidade avistada na natureza: 1

Pokemon(id=11, nome='Articuno', disponivel=1/1)
```

Antes de cadastrar, o sistema valida se o tipo, o habitat e a região informados
realmente existem — se algum id for inválido, o cadastro é recusado com uma
mensagem de erro em vez de gravar uma referência quebrada.

### 6. Vincular um Pokémon já existente a outro Habitat

```
Escolha uma opção: 6

-- Vincular Pokémon --
1-Vincular a Tipo  2-Vincular a Habitat  3-Vincular a Região
Opção: 2
ID do pokémon: 11
ID do habitat: 1

Pokemon(id=11, nome='Articuno', disponivel=1/1)
```

Essa é a operação de **associação entre entidades**: o mesmo menu permite
revincular um Pokémon a um Tipo, Habitat ou Região diferentes a qualquer momento.

### 7. Listar todas as capturas do sistema

```
Escolha uma opção: 8

Captura(id=1, pokemon_id=2, treinador_id=2, apelido='Charzinho', status='ATIVO')
```

Diferente do menu do treinador (que só mostra as próprias capturas), aqui o
administrador vê **todas** as capturas de **todos** os treinadores.

### 8. Registrar a libertação de um Pokémon (regra de negócio inversa)

```
Escolha uma opção: 9
ID da captura: 1

Captura(id=1, pokemon_id=2, treinador_id=2, apelido='Charzinho', status='LIBERTADO')
```

Assim como a captura, a libertação também atualiza duas entidades em uma única
operação:
1. o status da `Captura` muda para `LIBERTADO` e a data de libertação é gravada;
2. `qtd_disponivel` do Pokémon volta a subir (o exemplar retorna à natureza).

---

## Referência rápida de menus

| Perfil | Opções disponíveis |
|---|---|
| **Treinador** | Pesquisar Pokémon · Capturar Pokémon · Ver Minha Equipe |
| **Administrador** | CRUD de Tipos, Habitats, Regiões, Pokémons e Usuários · Vincular Pokémon · Pesquisar Pokémon · Listar todas as Capturas · Registrar Libertação |

Logins de exemplo (criados pelo `seed_dados.py`):

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@pokemanager.com | admin123 |
| Treinador | ash@pokemanager.com | treinador123 |
