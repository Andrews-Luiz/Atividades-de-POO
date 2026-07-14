class Usuario:
    def __init__(self, login, senha, nome, email, telefone):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def verificar_senha(self, senha):
        return self.senha == senha

    def __str__(self):
        return f"[{self.login}] {self.nome} | {self.email} | {self.telefone}"


class Cliente(Usuario):
    def __init__(self, login, senha, nome, email, telefone, cpf, endereco):
        super().__init__(login, senha, nome, email, telefone)
        self.cpf = cpf
        self.endereco = endereco
        self.carrinho = []
        self.compras = []

    def __str__(self):
        return (f"[Cliente] {self.nome} | Login: {self.login} | "
                f"CPF: {self.cpf} | Email: {self.email} | "
                f"Tel: {self.telefone} | End: {self.endereco}")


class Admin(Usuario):
    def __init__(self, login, senha, nome, email, telefone):
        super().__init__(login, senha, nome, email, telefone)

    def __str__(self):
        return f"[Admin] {self.nome} | Login: {self.login} | Email: {self.email}"