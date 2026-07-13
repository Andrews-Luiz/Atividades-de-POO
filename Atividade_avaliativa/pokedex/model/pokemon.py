class Pokemon:
    """
    Entidade Pokemon - pertence a um Tipo, a um Habitat e a uma Regiao
    (relacionamentos N para 1) e é alvo de Capturas (relacionamento 1 para N).
    """

    def __init__(self, nome, numero_pokedex, tipo_id, habitat_id, regiao_id,
                 hp_base, qtd_avistados, id=None, qtd_disponivel=None):
        self.id = id
        self.nome = nome
        self.numero_pokedex = numero_pokedex
        self.tipo_id = tipo_id
        self.habitat_id = habitat_id
        self.regiao_id = regiao_id
        self.hp_base = hp_base
        self.qtd_avistados = qtd_avistados
        # se não informado, ao cadastrar o pokémon todos os avistados estão disponíveis para captura
        self.qtd_disponivel = qtd_disponivel if qtd_disponivel is not None else qtd_avistados

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "numero_pokedex": self.numero_pokedex,
            "tipo_id": self.tipo_id,
            "habitat_id": self.habitat_id,
            "regiao_id": self.regiao_id,
            "hp_base": self.hp_base,
            "qtd_avistados": self.qtd_avistados,
            "qtd_disponivel": self.qtd_disponivel,
        }

    @staticmethod
    def from_dict(d):
        return Pokemon(
            nome=d["nome"],
            numero_pokedex=d["numero_pokedex"],
            tipo_id=d["tipo_id"],
            habitat_id=d["habitat_id"],
            regiao_id=d["regiao_id"],
            hp_base=d["hp_base"],
            qtd_avistados=d["qtd_avistados"],
            id=d.get("id"),
            qtd_disponivel=d.get("qtd_disponivel"),
        )

    def __repr__(self):
        return (f"Pokemon(id={self.id}, nome='{self.nome}', "
                f"disponivel={self.qtd_disponivel}/{self.qtd_avistados})")
