class Categoria:
    """Entidade Categoria - agrupa livros (relacionamento 1 para N com Livro)."""

    def __init__(self, nome, descricao="", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}

    @staticmethod
    def from_dict(d):
        return Categoria(nome=d["nome"], descricao=d.get("descricao", ""), id=d.get("id"))

    def __repr__(self):
        return f"Categoria(id={self.id}, nome='{self.nome}')"
