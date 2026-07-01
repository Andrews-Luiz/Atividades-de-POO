import json
import os


class RepositorioBase:
    """
    Repositório genérico responsável por ler e gravar listas de objetos
    em arquivos JSON. As subclasses definem o arquivo e a classe do modelo
    (via os métodos to_dict/from_dict do próprio objeto).
    """

    def __init__(self, arquivo, classe_modelo, pasta_dados="data"):
        os.makedirs(pasta_dados, exist_ok=True)
        self.caminho = os.path.join(pasta_dados, arquivo)
        self.classe_modelo = classe_modelo
        if not os.path.exists(self.caminho):
            self._salvar_lista_dict([])

    # ---------- operações de baixo nível (arquivo) ----------
    def _carregar_lista_dict(self):
        with open(self.caminho, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            return json.loads(conteudo) if conteudo else []

    def _salvar_lista_dict(self, lista_dict):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(lista_dict, f, ensure_ascii=False, indent=2)

    # ---------- operações de alto nível (objetos do modelo) ----------
    def carregar_todos(self):
        return [self.classe_modelo.from_dict(d) for d in self._carregar_lista_dict()]

    def salvar_todos(self, lista_objetos):
        self._salvar_lista_dict([obj.to_dict() for obj in lista_objetos])

    def proximo_id(self):
        objetos = self.carregar_todos()
        if not objetos:
            return 1
        return max(o.id for o in objetos) + 1

    # ---------- CRUD genérico ----------
    def inserir(self, objeto):
        objetos = self.carregar_todos()
        objeto.id = self.proximo_id()
        objetos.append(objeto)
        self.salvar_todos(objetos)
        return objeto

    def listar(self):
        return self.carregar_todos()

    def buscar_por_id(self, id):
        for o in self.carregar_todos():
            if o.id == id:
                return o
        return None

    def atualizar(self, objeto):
        objetos = self.carregar_todos()
        for i, o in enumerate(objetos):
            if o.id == objeto.id:
                objetos[i] = objeto
                self.salvar_todos(objetos)
                return True
        return False

    def excluir(self, id):
        objetos = self.carregar_todos()
        novos = [o for o in objetos if o.id != id]
        if len(novos) == len(objetos):
            return False
        self.salvar_todos(novos)
        return True
