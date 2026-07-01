class Livro:
    """
    Entidade Livro - pertence a uma Categoria, a um Autor e a uma Editora
    (relacionamentos N para 1) e gera Emprestimos (relacionamento 1 para N).
    """

    def __init__(self, titulo, isbn, categoria_id, autor_id, editora_id, qtd_total,
                 id=None, qtd_disponivel=None):
        self.id = id
        self.titulo = titulo
        self.isbn = isbn
        self.categoria_id = categoria_id
        self.autor_id = autor_id
        self.editora_id = editora_id
        self.qtd_total = qtd_total
        # se não informado, ao criar um livro novo toda a quantidade está disponível
        self.qtd_disponivel = qtd_disponivel if qtd_disponivel is not None else qtd_total

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "isbn": self.isbn,
            "categoria_id": self.categoria_id,
            "autor_id": self.autor_id,
            "editora_id": self.editora_id,
            "qtd_total": self.qtd_total,
            "qtd_disponivel": self.qtd_disponivel,
        }

    @staticmethod
    def from_dict(d):
        return Livro(
            titulo=d["titulo"],
            isbn=d["isbn"],
            categoria_id=d["categoria_id"],
            autor_id=d["autor_id"],
            editora_id=d["editora_id"],
            qtd_total=d["qtd_total"],
            id=d.get("id"),
            qtd_disponivel=d.get("qtd_disponivel"),
        )

    def __repr__(self):
        return (f"Livro(id={self.id}, titulo='{self.titulo}', "
                f"disponivel={self.qtd_disponivel}/{self.qtd_total})")
