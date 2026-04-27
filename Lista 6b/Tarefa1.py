import datetime


class Cliente:
    def __init__(self, id: int, n: str, e: str, f: str):
        self.__id = id
        self.__nome = n
        self.__email = e
        self.__fone = f

    # Getters
    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_fone(self):
        return self.__fone

    # Setters
    def set_nome(self, nome: str):
        self.__nome = nome

    def set_email(self, email: str):
        self.__email = email

    def set_fone(self, fone: str):
        self.__fone = fone

    def __str__(self):
        return (f"Cliente[id={self.__id}, nome={self.__nome}, "
                f"email={self.__email}, fone={self.__fone}]")


class Categoria:
    def __init__(self, id: int, d: str):
        self.__id = id
        self.__descricao = d

    # Getters
    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    # Setters
    def set_descricao(self, descricao: str):
        self.__descricao = descricao

    def __str__(self):
        return f"Categoria[id={self.__id}, descricao={self.__descricao}]"


class Produto:
    def __init__(self, id: int, d: str, p: float, e: int):
        self.__id = id
        self.__descricao = d
        self.__preco = p
        self.__estoque = e
        self.__idCategoria = None

    # Getters
    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def get_preco(self):
        return self.__preco

    def get_estoque(self):
        return self.__estoque

    def get_idCategoria(self):
        return self.__idCategoria

    # Setters
    def set_descricao(self, descricao: str):
        self.__descricao = descricao

    def set_preco(self, preco: float):
        self.__preco = preco

    def set_estoque(self, estoque: int):
        self.__estoque = estoque

    def set_idCategoria(self, idCategoria: int):
        self.__idCategoria = idCategoria

    def __str__(self):
        return (f"Produto[id={self.__id}, descricao={self.__descricao}, "
                f"preco={self.__preco:.2f}, estoque={self.__estoque}, "
                f"idCategoria={self.__idCategoria}]")


class Venda:
    def __init__(self, id: int):
        self.__id = id
        self.__data = datetime.datetime.now()
        self.__carrinho = []
        self.__total = 0.0
        self.__idCliente = None

    # Getters
    def get_id(self):
        return self.__id

    def get_data(self):
        return self.__data

    def get_carrinho(self):
        return self.__carrinho

    def get_total(self):
        return self.__total

    def get_idCliente(self):
        return self.__idCliente

    # Setters
    def set_data(self, data: datetime.datetime):
        self.__data = data

    def set_total(self, total: float):
        self.__total = total

    def set_idCliente(self, idCliente: int):
        self.__idCliente = idCliente

    def set_carrinho(self, carrinho: list):
        self.__carrinho = carrinho

    def __str__(self):
        return (f"Venda[id={self.__id}, data={self.__data.strftime('%d/%m/%Y %H:%M')}, "
                f"total=R${self.__total:.2f}, idCliente={self.__idCliente}]")


class VendaItem:
    def __init__(self, id: int, q: int, p: double if False else float):
        self.__id = id
        self.__qtd = q
        self.__preco = p
        self.__idVenda = None
        self.__idProduto = None

    # Getters
    def get_id(self):
        return self.__id

    def get_qtd(self):
        return self.__qtd

    def get_preco(self):
        return self.__preco

    def get_idVenda(self):
        return self.__idVenda

    def get_idProduto(self):
        return self.__idProduto

    # Setters
    def set_qtd(self, qtd: int):
        self.__qtd = qtd

    def set_preco(self, preco: float):
        self.__preco = preco

    def set_idVenda(self, idVenda: int):
        self.__idVenda = idVenda

    def set_idProduto(self, idProduto: int):
        self.__idProduto = idProduto

    def __str__(self):
        return (f"VendaItem[id={self.__id}, qtd={self.__qtd}, "
                f"preco=R${self.__preco:.2f}, idVenda={self.__idVenda}, "
                f"idProduto={self.__idProduto}]")


# ─────────────────────────────────────────
# Teste das classes
# ─────────────────────────────────────────
if __name__ == "__main__":
    # Cliente
    cliente = Cliente(1, "Maria Silva", "maria@email.com", "84999990000")
    print(cliente)

    # Categoria
    categoria = Categoria(1, "Eletrônicos")
    print(categoria)

    # Produto
    produto = Produto(1, "Smartphone XYZ", 1999.90, 50)
    produto.set_idCategoria(categoria.get_id())
    print(produto)

    # VendaItem
    item = VendaItem(1, 2, produto.get_preco())
    item.set_idProduto(produto.get_id())
    item.set_idVenda(1)
    print(item)

    # Venda
    venda = Venda(1)
    venda.set_idCliente(cliente.get_id())
    venda.set_total(item.get_qtd() * item.get_preco())
    venda.set_carrinho([item])
    print(venda)