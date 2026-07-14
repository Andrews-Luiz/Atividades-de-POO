from model.habitat import Habitat
from persistence.habitat_repositorio import HabitatRepositorio


class HabitatService:
    def __init__(self):
        self.repositorio = HabitatRepositorio()

    def cadastrar(self, nome, descricao=""):
        habitat = Habitat(nome=nome, descricao=descricao)
        return self.repositorio.inserir(habitat)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, habitat):
        return self.repositorio.atualizar(habitat)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
