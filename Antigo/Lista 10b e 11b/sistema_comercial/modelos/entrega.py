class Entrega:
    def __init__(self, id, venda, entregador):
        self.id = id
        self.venda = venda
        self.entregador = entregador
        self.status = "Pendente"

    def __str__(self):
        return f"Entrega #{self.id} | Venda #{self.venda.id} | Status: {self.status}"