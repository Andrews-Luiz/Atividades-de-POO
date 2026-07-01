from model.categoria import Categoria
from persistence.categoria_repositorio import CategoriaRepositorio


class CategoriaService:
    def __init__(self):
        self.repositorio = CategoriaRepositorio()

    def cadastrar(self, nome, descricao=""):
        categoria = Categoria(nome=nome, descricao=descricao)
        return self.repositorio.inserir(categoria)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, categoria):
        return self.repositorio.atualizar(categoria)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
