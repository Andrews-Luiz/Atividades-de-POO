from model.autor import Autor
from persistence.autor_repositorio import AutorRepositorio


class AutorService:
    def __init__(self):
        self.repositorio = AutorRepositorio()

    def cadastrar(self, nome, nacionalidade=""):
        autor = Autor(nome=nome, nacionalidade=nacionalidade)
        return self.repositorio.inserir(autor)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, autor):
        return self.repositorio.atualizar(autor)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
