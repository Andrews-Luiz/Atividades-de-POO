from pokedex.model.regiao import Regiao
from pokedex.persistence.regiao_repositorio import RegiaoRepositorio


class RegiaoService:
    def __init__(self):
        self.repositorio = RegiaoRepositorio()

    def cadastrar(self, nome, descricao=""):
        regiao = Regiao(nome=nome, descricao=descricao)
        return self.repositorio.inserir(regiao)

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, regiao):
        return self.repositorio.atualizar(regiao)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_nome(self, termo):
        return self.repositorio.pesquisar_por_nome(termo)
