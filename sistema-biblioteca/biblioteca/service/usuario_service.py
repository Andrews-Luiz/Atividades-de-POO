from model.usuario import Usuario
from persistence.usuario_repositorio import UsuarioRepositorio


class UsuarioService:
    def __init__(self):
        self.repositorio = UsuarioRepositorio()

    def cadastrar(self, nome, email, senha, perfil):
        if self.repositorio.buscar_por_email(email):
            raise ValueError("Já existe um usuário cadastrado com esse e-mail.")
        usuario = Usuario(nome=nome, email=email, senha=senha, perfil=perfil)
        return self.repositorio.inserir(usuario)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, usuario):
        return self.repositorio.atualizar(usuario)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)

    def autenticar(self, email, senha):
        """Regra de negócio de login: valida credenciais e retorna o usuário autenticado."""
        usuario = self.repositorio.buscar_por_email(email)
        if usuario and usuario.senha == senha:
            return usuario
        return None
