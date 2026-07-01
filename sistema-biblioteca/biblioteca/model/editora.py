class Editora:
    """Entidade Editora - uma editora pode ter vários livros (relacionamento 1 para N com Livro)."""

    def __init__(self, nome, cidade="", id=None):
        self.id = id
        self.nome = nome
        self.cidade = cidade

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "cidade": self.cidade}

    @staticmethod
    def from_dict(d):
        return Editora(nome=d["nome"], cidade=d.get("cidade", ""), id=d.get("id"))

    def __repr__(self):
        return f"Editora(id={self.id}, nome='{self.nome}')"
