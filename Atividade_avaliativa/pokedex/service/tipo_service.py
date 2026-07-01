from model.tipo import Tipo
from persistence.tipo_repositorio import TipoRepositorio


class TipoService:
    def __init__(self):
        self.repositorio = TipoRepositorio()

    def cadastrar(self, nome, descricao=""):
        tipo = Tipo(nome=nome, descricao=descricao)
        return self.repositorio.inserir(tipo)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, tipo):
        return self.repositorio.atualizar(tipo)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
