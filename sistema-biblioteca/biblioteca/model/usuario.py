class Usuario:
    """Entidade Usuario - controla o login e o perfil de acesso ao sistema."""

    PERFIL_ADMIN = "admin"
    PERFIL_LEITOR = "leitor"

    def __init__(self, nome, email, senha, perfil, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfil = perfil  # "admin" ou "leitor"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "perfil": self.perfil,
        }

    @staticmethod
    def from_dict(d):
        return Usuario(
            nome=d["nome"],
            email=d["email"],
            senha=d["senha"],
            perfil=d["perfil"],
            id=d.get("id"),
        )

    def __repr__(self):
        return f"Usuario(id={self.id}, nome='{self.nome}', perfil='{self.perfil}')"
