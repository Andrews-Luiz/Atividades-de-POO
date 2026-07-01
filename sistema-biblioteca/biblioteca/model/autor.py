class Autor:
    """Entidade Autor - um autor pode ter vários livros (relacionamento 1 para N com Livro)."""

    def __init__(self, nome, nacionalidade="", id=None):
        self.id = id
        self.nome = nome
        self.nacionalidade = nacionalidade

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "nacionalidade": self.nacionalidade}

    @staticmethod
    def from_dict(d):
        return Autor(nome=d["nome"], nacionalidade=d.get("nacionalidade", ""), id=d.get("id"))

    def __repr__(self):
        return f"Autor(id={self.id}, nome='{self.nome}')"
