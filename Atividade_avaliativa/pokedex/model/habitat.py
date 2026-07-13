class Habitat:
    """Entidade Habitat - ambiente natural onde um Pokémon é encontrado
    (Floresta, Caverna, Oceano...). Um Habitat pode ter vários Pokémon (1 para N)."""

    def __init__(self, nome, descricao="", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}

    @staticmethod
    def from_dict(d):
        return Habitat(nome=d["nome"], descricao=d.get("descricao", ""), id=d.get("id"))

    def __repr__(self):
        return f"Habitat(id={self.id}, nome='{self.nome}')"
