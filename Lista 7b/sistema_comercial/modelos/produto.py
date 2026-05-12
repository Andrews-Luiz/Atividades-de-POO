class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def __str__(self):
        return f"{self.id} - {self.nome}"


class Produto:
    def __init__(self, id, nome, preco, quantidade, categoria):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria = categoria

    def __str__(self):
        return (f"ID: {self.id} | {self.nome} | "
                f"Preco: R${self.preco:.2f} | "
                f"Qtd: {self.quantidade} | "
                f"Categoria: {self.categoria.nome}")