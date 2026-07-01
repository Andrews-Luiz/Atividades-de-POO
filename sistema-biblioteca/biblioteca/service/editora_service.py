from model.editora import Editora
from persistence.editora_repositorio import EditoraRepositorio


class EditoraService:
    def __init__(self):
        self.repositorio = EditoraRepositorio()

    def cadastrar(self, nome, cidade=""):
        editora = Editora(nome=nome, cidade=cidade)
        return self.repositorio.inserir(editora)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, editora):
        return self.repositorio.atualizar(editora)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
