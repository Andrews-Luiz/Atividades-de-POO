from model.usuario import Usuario
from persistence.repositorio_base import RepositorioBase


class UsuarioRepositorio(RepositorioBase):
    def __init__(self, pasta_dados="data"):
        super().__init__("usuarios.json", Usuario, pasta_dados)

    def pesquisar_por_nome(self, termo):
        termo = termo.lower()
        return [u for u in self.carregar_todos() if termo in u.nome.lower()]

    def buscar_por_email(self, email):
        for u in self.carregar_todos():
            if u.email.lower() == email.lower():
                return u
        return None
