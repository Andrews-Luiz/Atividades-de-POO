"""
Testes de persistência: verificam se é possível salvar e ler
objetos das classes do modelo em arquivo JSON, além de validar
uma regra de negócio que envolve mais de uma entidade.

Execução: python3 -m unittest tests.test_persistencia -v
(a partir da raiz do projeto)
"""
import os
import shutil
import unittest

from model.usuario import Usuario
from model.categoria import Categoria
from model.autor import Autor
from model.editora import Editora
from model.livro import Livro
from model.emprestimo import Emprestimo

from persistence.usuario_repositorio import UsuarioRepositorio
from persistence.categoria_repositorio import CategoriaRepositorio
from persistence.autor_repositorio import AutorRepositorio
from persistence.editora_repositorio import EditoraRepositorio
from persistence.livro_repositorio import LivroRepositorio
from persistence.emprestimo_repositorio import EmprestimoRepositorio

from service.emprestimo_service import EmprestimoService
from service.livro_service import LivroService
from service.usuario_service import UsuarioService
from service.categoria_service import CategoriaService
from service.autor_service import AutorService
from service.editora_service import EditoraService

PASTA_TESTE = "data_teste"


class TestPersistenciaUsuario(unittest.TestCase):
    def setUp(self):
        self.repo = UsuarioRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_usuario(self):
        usuario = Usuario(nome="Ana Souza", email="ana@email.com",
                           senha="123456", perfil=Usuario.PERFIL_LEITOR)
        usuario_salvo = self.repo.inserir(usuario)
        self.assertIsNotNone(usuario_salvo.id)

        # Simula reabertura do sistema: cria um novo repositório e lê do arquivo
        repo2 = UsuarioRepositorio(pasta_dados=PASTA_TESTE)
        usuarios = repo2.listar()

        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nome, "Ana Souza")
        self.assertEqual(usuarios[0].email, "ana@email.com")
        self.assertEqual(usuarios[0].perfil, Usuario.PERFIL_LEITOR)


class TestPersistenciaCategoria(unittest.TestCase):
    def setUp(self):
        self.repo = CategoriaRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_categoria(self):
        categoria = Categoria(nome="Ficção Científica", descricao="Livros de FC")
        self.repo.inserir(categoria)

        repo2 = CategoriaRepositorio(pasta_dados=PASTA_TESTE)
        categorias = repo2.listar()

        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0].nome, "Ficção Científica")


class TestPersistenciaAutor(unittest.TestCase):
    def setUp(self):
        self.repo = AutorRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_autor(self):
        autor = Autor(nome="Frank Herbert", nacionalidade="Norte-americano")
        self.repo.inserir(autor)

        repo2 = AutorRepositorio(pasta_dados=PASTA_TESTE)
        autores = repo2.listar()

        self.assertEqual(len(autores), 1)
        self.assertEqual(autores[0].nome, "Frank Herbert")


class TestPersistenciaEditora(unittest.TestCase):
    def setUp(self):
        self.repo = EditoraRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_editora(self):
        editora = Editora(nome="Aleph", cidade="São Paulo")
        self.repo.inserir(editora)

        repo2 = EditoraRepositorio(pasta_dados=PASTA_TESTE)
        editoras = repo2.listar()

        self.assertEqual(len(editoras), 1)
        self.assertEqual(editoras[0].nome, "Aleph")


class TestPersistenciaLivro(unittest.TestCase):
    def setUp(self):
        self.repo = LivroRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_livro(self):
        livro = Livro(titulo="Duna", isbn="978-0-01", categoria_id=1,
                       autor_id=1, editora_id=1, qtd_total=3)
        self.repo.inserir(livro)

        repo2 = LivroRepositorio(pasta_dados=PASTA_TESTE)
        livros = repo2.listar()

        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0].titulo, "Duna")
        self.assertEqual(livros[0].qtd_disponivel, 3)  # criado igual à qtd_total

    def test_atualizar_e_excluir_livro(self):
        livro = self.repo.inserir(Livro(titulo="1984", isbn="978-0-02",
                                         categoria_id=1, autor_id=1, editora_id=1, qtd_total=2))
        livro.qtd_disponivel = 1
        self.assertTrue(self.repo.atualizar(livro))

        recarregado = self.repo.buscar_por_id(livro.id)
        self.assertEqual(recarregado.qtd_disponivel, 1)

        self.assertTrue(self.repo.excluir(livro.id))
        self.assertIsNone(self.repo.buscar_por_id(livro.id))


class TestPersistenciaEmprestimo(unittest.TestCase):
    def setUp(self):
        self.repo = EmprestimoRepositorio(pasta_dados=PASTA_TESTE)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_salvar_e_ler_emprestimo(self):
        emprestimo = Emprestimo(livro_id=1, usuario_id=1,
                                 data_emprestimo="2026-07-01",
                                 data_devolucao_prevista="2026-07-08")
        self.repo.inserir(emprestimo)

        repo2 = EmprestimoRepositorio(pasta_dados=PASTA_TESTE)
        emprestimos = repo2.listar()

        self.assertEqual(len(emprestimos), 1)
        self.assertEqual(emprestimos[0].status, Emprestimo.STATUS_ATIVO)


class TestRegraDeNegocioEmprestimo(unittest.TestCase):
    """
    Testa a regra de negócio que manipula objetos de mais de uma entidade
    em uma mesma operação: ao realizar um empréstimo, o sistema insere um
    registro em Emprestimo e atualiza a quantidade disponível em Livro.
    O mesmo vale para a devolução (operação inversa).
    """

    def setUp(self):
        os.makedirs(PASTA_TESTE, exist_ok=True)

        self.usuario_service = UsuarioService()
        self.usuario_service.repositorio = UsuarioRepositorio(pasta_dados=PASTA_TESTE)

        self.categoria_service = CategoriaService()
        self.categoria_service.repositorio = CategoriaRepositorio(pasta_dados=PASTA_TESTE)

        self.autor_service = AutorService()
        self.autor_service.repositorio = AutorRepositorio(pasta_dados=PASTA_TESTE)

        self.editora_service = EditoraService()
        self.editora_service.repositorio = EditoraRepositorio(pasta_dados=PASTA_TESTE)

        self.livro_service = LivroService()
        self.livro_service.repositorio = LivroRepositorio(pasta_dados=PASTA_TESTE)
        self.livro_service.repositorio_categoria = self.categoria_service.repositorio
        self.livro_service.repositorio_autor = self.autor_service.repositorio
        self.livro_service.repositorio_editora = self.editora_service.repositorio

        self.emprestimo_service = EmprestimoService()
        self.emprestimo_service.repositorio = EmprestimoRepositorio(pasta_dados=PASTA_TESTE)
        self.emprestimo_service.repositorio_livro = self.livro_service.repositorio
        self.emprestimo_service.repositorio_usuario = self.usuario_service.repositorio

        self.categoria = self.categoria_service.cadastrar("Romance", "Livros de romance")
        self.autor = self.autor_service.cadastrar("Machado de Assis", "Brasileiro")
        self.editora = self.editora_service.cadastrar("Penguin", "São Paulo")
        self.usuario = self.usuario_service.cadastrar(
            "Carlos Lima", "carlos@email.com", "senha123", Usuario.PERFIL_LEITOR)
        self.livro = self.livro_service.cadastrar(
            "Dom Casmurro", "978-0-03", self.categoria.id, self.autor.id, self.editora.id, qtd_total=1)

    def tearDown(self):
        shutil.rmtree(PASTA_TESTE, ignore_errors=True)

    def test_emprestimo_diminui_disponibilidade_do_livro(self):
        self.assertEqual(self.livro.qtd_disponivel, 1)

        self.emprestimo_service.realizar_emprestimo(self.livro.id, self.usuario.id)

        livro_atualizado = self.livro_service.buscar_por_id(self.livro.id)
        self.assertEqual(livro_atualizado.qtd_disponivel, 0)

    def test_nao_permite_emprestimo_sem_exemplar_disponivel(self):
        self.emprestimo_service.realizar_emprestimo(self.livro.id, self.usuario.id)
        with self.assertRaises(ValueError):
            self.emprestimo_service.realizar_emprestimo(self.livro.id, self.usuario.id)

    def test_devolucao_restaura_disponibilidade_do_livro(self):
        emprestimo = self.emprestimo_service.realizar_emprestimo(self.livro.id, self.usuario.id)
        self.emprestimo_service.registrar_devolucao(emprestimo.id)

        livro_atualizado = self.livro_service.buscar_por_id(self.livro.id)
        self.assertEqual(livro_atualizado.qtd_disponivel, 1)

        emprestimo_atualizado = self.emprestimo_service.buscar_por_id(emprestimo.id)
        self.assertEqual(emprestimo_atualizado.status, Emprestimo.STATUS_DEVOLVIDO)
        self.assertIsNotNone(emprestimo_atualizado.data_devolucao_real)

    def test_vincular_livro_a_outro_autor(self):
        novo_autor = self.autor_service.cadastrar("José de Alencar", "Brasileiro")
        livro_atualizado = self.livro_service.vincular_autor(self.livro.id, novo_autor.id)
        self.assertEqual(livro_atualizado.autor_id, novo_autor.id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
