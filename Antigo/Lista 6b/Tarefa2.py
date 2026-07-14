import json
import datetime
from Tarefa1 import Cliente, Categoria, Produto, Venda, VendaItem

# As classes DAO(Data Object Acess) são responsáveis por persistir os dados. 
# Cada uma mantendo uma lista estática dos objetos do modelo


# ClienteDAO

class ClienteDAO:
    objetos: list = []

    @classmethod
    def Inserir(cls, obj: Cliente) -> None: # O método inserir adiciona um objeto à lista
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls) -> list: # Listar retorna todos os objetos da lista
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> Cliente: # Listar_ID busca um objeto especifico
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj: Cliente) -> None: # Atualizar serve para substituir um objeto na lista
        for i, c in enumerate(cls.objetos):
            if c.get_id() == obj.get_id():
                cls.objetos[i] = obj
                return

    @classmethod
    def Excluir(cls, obj: Cliente) -> None: # Excluir remove um objeto da lista
        cls.objetos = [c for c in cls.objetos if c.get_id() != obj.get_id()]

# Os métodos salvar e abrir abaixo, gravam e leem essa lista em um arquivo Json
# Isso serve para garantir a proteção dos dados quando o arquivo fechar
# Json é um arquivo de texto simples, utilizado para estruturar e transportar informações

    @classmethod
    def Abrir(cls) -> None: 
        try:
            with open("clientes.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = []
                for d in dados:
                    c = Cliente(d["id"], d["nome"], d["email"], d["fone"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        dados = []
        for c in cls.objetos:
            dados.append({
                "id": c.get_id(),
                "nome": c.get_nome(),
                "email": c.get_email(),
                "fone": c.get_fone()
            })
        with open("clientes.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────
# CategoriaDAO
# ─────────────────────────────────────────
class CategoriaDAO:
    objetos: list = []

    @classmethod
    def Inserir(cls, obj: Categoria) -> None:
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls) -> list:
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> Categoria:
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj: Categoria) -> None:
        for i, c in enumerate(cls.objetos):
            if c.get_id() == obj.get_id():
                cls.objetos[i] = obj
                return

    @classmethod
    def Excluir(cls, obj: Categoria) -> None:
        cls.objetos = [c for c in cls.objetos if c.get_id() != obj.get_id()]

    @classmethod
    def Abrir(cls) -> None:
        try:
            with open("categorias.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = []
                for d in dados:
                    c = Categoria(d["id"], d["descricao"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        dados = []
        for c in cls.objetos:
            dados.append({
                "id": c.get_id(),
                "descricao": c.get_descricao()
            })
        with open("categorias.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────
# ProdutoDAO
# ─────────────────────────────────────────
class ProdutoDAO:
    objetos: list = []

    @classmethod
    def Inserir(cls, obj: Produto) -> None:
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls) -> list:
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> Produto:
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj: Produto) -> None:
        for i, p in enumerate(cls.objetos):
            if p.get_id() == obj.get_id():
                cls.objetos[i] = obj
                return

    @classmethod
    def Excluir(cls, obj: Produto) -> None:
        cls.objetos = [p for p in cls.objetos if p.get_id() != obj.get_id()]

    @classmethod
    def Abrir(cls) -> None:
        try:
            with open("produtos.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = []
                for d in dados:
                    p = Produto(d["id"], d["descricao"], d["preco"], d["estoque"])
                    p.set_idCategoria(d["idCategoria"])
                    cls.objetos.append(p)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        dados = []
        for p in cls.objetos:
            dados.append({
                "id": p.get_id(),
                "descricao": p.get_descricao(),
                "preco": p.get_preco(),
                "estoque": p.get_estoque(),
                "idCategoria": p.get_idCategoria()
            })
        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────
# VendaDAO
# ─────────────────────────────────────────
class VendaDAO:
    objetos: list = []

    @classmethod
    def Inserir(cls, obj: Venda) -> None:
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls) -> list:
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> Venda:
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj: Venda) -> None:
        for i, v in enumerate(cls.objetos):
            if v.get_id() == obj.get_id():
                cls.objetos[i] = obj
                return

    @classmethod
    def Excluir(cls, obj: Venda) -> None:
        cls.objetos = [v for v in cls.objetos if v.get_id() != obj.get_id()]

    @classmethod
    def Abrir(cls) -> None:
        try:
            with open("vendas.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = []
                for d in dados:
                    v = Venda(d["id"])
                    v.set_data(datetime.datetime.fromisoformat(d["data"]))
                    v.set_total(d["total"])
                    v.set_idCliente(d["idCliente"])
                    cls.objetos.append(v)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        dados = []
        for v in cls.objetos:
            dados.append({
                "id": v.get_id(),
                "data": v.get_data().isoformat(),
                "total": v.get_total(),
                "idCliente": v.get_idCliente()
            })
        with open("vendas.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────
# VendaItemDAO
# ─────────────────────────────────────────
class VendaItemDAO:
    objetos: list = []

    @classmethod
    def Inserir(cls, obj: VendaItem) -> None:
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls) -> list:
        return cls.objetos

    @classmethod
    def Listar_Id(cls, id: int) -> VendaItem:
        for obj in cls.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj: VendaItem) -> None:
        for i, vi in enumerate(cls.objetos):
            if vi.get_id() == obj.get_id():
                cls.objetos[i] = obj
                return

    @classmethod
    def Excluir(cls, obj: VendaItem) -> None:
        cls.objetos = [vi for vi in cls.objetos if vi.get_id() != obj.get_id()]

    @classmethod
    def Abrir(cls) -> None:
        try:
            with open("vendaitens.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                cls.objetos = []
                for d in dados:
                    vi = VendaItem(d["id"], d["qtd"], d["preco"])
                    vi.set_idVenda(d["idVenda"])
                    vi.set_idProduto(d["idProduto"])
                    cls.objetos.append(vi)
        except FileNotFoundError:
            cls.objetos = []

    @classmethod
    def Salvar(cls) -> None:
        dados = []
        for vi in cls.objetos:
            dados.append({
                "id": vi.get_id(),
                "qtd": vi.get_qtd(),
                "preco": vi.get_preco(),
                "idVenda": vi.get_idVenda(),
                "idProduto": vi.get_idProduto()
            })
        with open("vendaitens.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ─────────────────────────────────────────
# Testes
# ─────────────────────────────────────────
if __name__ == "__main__":
    # --- Clientes ---
    print("=== CLIENTES ===")
    c1 = Cliente(1, "Maria Silva", "maria@email.com", "84999990000")
    c2 = Cliente(2, "João Souza", "joao@email.com", "84988880000")
    ClienteDAO.Inserir(c1)
    ClienteDAO.Inserir(c2)
    for c in ClienteDAO.Listar():
        print(c)

    print("\nBuscando id=2:", ClienteDAO.Listar_Id(2))

    c2.set_email("joao_novo@email.com")
    ClienteDAO.Atualizar(c2)
    print("Após atualizar e-mail:", ClienteDAO.Listar_Id(2))

    ClienteDAO.Salvar()
    ClienteDAO.objetos = []
    ClienteDAO.Abrir()
    print("Após Salvar e Abrir:", [str(c) for c in ClienteDAO.Listar()])

    # --- Categorias ---
    print("\n=== CATEGORIAS ===")
    cat1 = Categoria(1, "Eletrônicos")
    CategoriaDAO.Inserir(cat1)
    CategoriaDAO.Salvar()
    CategoriaDAO.objetos = []
    CategoriaDAO.Abrir()
    print(CategoriaDAO.Listar_Id(1))

    # --- Produtos ---
    print("\n=== PRODUTOS ===")
    p1 = Produto(1, "Smartphone XYZ", 1999.90, 50)
    p1.set_idCategoria(1)
    ProdutoDAO.Inserir(p1)
    ProdutoDAO.Salvar()
    ProdutoDAO.objetos = []
    ProdutoDAO.Abrir()
    print(ProdutoDAO.Listar_Id(1))

    # --- Vendas ---
    print("\n=== VENDAS ===")
    v1 = Venda(1)
    v1.set_idCliente(1)
    v1.set_total(1999.90)
    VendaDAO.Inserir(v1)
    VendaDAO.Salvar()
    VendaDAO.objetos = []
    VendaDAO.Abrir()
    print(VendaDAO.Listar_Id(1))

    # --- VendaItens ---
    print("\n=== VENDAITENS ===")
    vi1 = VendaItem(1, 2, 1999.90)
    vi1.set_idVenda(1)
    vi1.set_idProduto(1)
    VendaItemDAO.Inserir(vi1)
    VendaItemDAO.Salvar()
    VendaItemDAO.objetos = []
    VendaItemDAO.Abrir()
    print(VendaItemDAO.Listar_Id(1))

    # --- Excluir ---
    print("\n=== EXCLUINDO cliente id=1 ===")
    ClienteDAO.Excluir(c1)
    print("Clientes restantes:", [str(c) for c in ClienteDAO.Listar()])