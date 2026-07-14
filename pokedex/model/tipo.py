class Tipo:
    """Entidade Tipo - tipo elemental de um Pokémon (Fogo, Água, Grama...).
    Um Tipo pode estar associado a vários Pokémon (1 para N)."""

    def __init__(self, nome, descricao="", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}

    @staticmethod
    def from_dict(d):
        return Tipo(nome=d["nome"], descricao=d.get("descricao", ""), id=d.get("id"))

    def __repr__(self):
        return f"Tipo(id={self.id}, nome='{self.nome}')"
