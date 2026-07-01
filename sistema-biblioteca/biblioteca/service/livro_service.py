from model.livro import Livro
from persistence.livro_repositorio import LivroRepositorio
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.autor_repositorio import AutorRepositorio
from persistence.editora_repositorio import EditoraRepositorio


class LivroService:
    def __init__(self):
        self.repositorio = LivroRepositorio()
        self.repositorio_categoria = CategoriaRepositorio()
        self.repositorio_autor = AutorRepositorio()
        self.repositorio_editora = EditoraRepositorio()

    def cadastrar(self, titulo, isbn, categoria_id, autor_id, editora_id, qtd_total):
        # Operações de associação: valida se categoria, autor e editora existem antes de vincular
        if categoria_id is not None and not self.repositorio_categoria.buscar_por_id(categoria_id):
            raise ValueError("Categoria informada não existe.")
        if autor_id is not None and not self.repositorio_autor.buscar_por_id(autor_id):
            raise ValueError("Autor informado não existe.")
        if editora_id is not None and not self.repositorio_editora.buscar_por_id(editora_id):
            raise ValueError("Editora informada não existe.")

        livro = Livro(titulo=titulo, isbn=isbn, categoria_id=categoria_id,
                       autor_id=autor_id, editora_id=editora_id, qtd_total=qtd_total)
        return self.repositorio.inserir(livro)

    def vincular_categoria(self, livro_id, categoria_id):
        """Operação de associação: vincula um livro já existente a uma categoria."""
        livro = self._buscar_livro_existente(livro_id)
        if not self.repositorio_categoria.buscar_por_id(categoria_id):
            raise ValueError("Categoria não encontrada.")
        livro.categoria_id = categoria_id
        self.repositorio.atualizar(livro)
        return livro

    def vincular_autor(self, livro_id, autor_id):
        """Operação de associação: vincula um livro já existente a um autor."""
        livro = self._buscar_livro_existente(livro_id)
        if not self.repositorio_autor.buscar_por_id(autor_id):
            raise ValueError("Autor não encontrado.")
        livro.autor_id = autor_id
        self.repositorio.atualizar(livro)
        return livro

    def vincular_editora(self, livro_id, editora_id):
        """Operação de associação: vincula um livro já existente a uma editora."""
        livro = self._buscar_livro_existente(livro_id)
        if not self.repositorio_editora.buscar_por_id(editora_id):
            raise ValueError("Editora não encontrada.")
        livro.editora_id = editora_id
        self.repositorio.atualizar(livro)
        return livro

    def _buscar_livro_existente(self, livro_id):
        livro = self.repositorio.buscar_por_id(livro_id)
        if not livro:
            raise ValueError("Livro não encontrado.")
        return livro

    def listar(self):
        return self.repositorio.listar()

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def atualizar(self, livro):
        return self.repositorio.atualizar(livro)

    def excluir(self, id):
        return self.repositorio.excluir(id)

    def pesquisar_por_titulo(self, termo):
        return self.repositorio.pesquisar_por_titulo(termo)
