"""
Script para popular o sistema com dados de exemplo (opcional).
Cria um admin, um leitor, categorias, autores, editoras e livros para
testar o sistema via main.py sem precisar cadastrar tudo manualmente.

Execução: python3 seed_dados.py
"""
from service.usuario_service import UsuarioService
from service.categoria_service import CategoriaService
from service.autor_service import AutorService
from service.editora_service import EditoraService
from service.livro_service import LivroService
from model.usuario import Usuario

usuario_service = UsuarioService()
categoria_service = CategoriaService()
autor_service = AutorService()
editora_service = EditoraService()
livro_service = LivroService()

print("Criando usuários de exemplo...")
try:
    usuario_service.cadastrar("Admin Geral", "admin@biblioteca.com", "admin123", Usuario.PERFIL_ADMIN)
except ValueError as e:
    print(f"  (aviso) {e}")
try:
    usuario_service.cadastrar("Maria Leitora", "maria@email.com", "leitor123", Usuario.PERFIL_LEITOR)
except ValueError as e:
    print(f"  (aviso) {e}")

print("Criando categorias de exemplo...")
cat_ficcao = categoria_service.cadastrar("Ficção Científica", "Livros de ficção científica")
cat_romance = categoria_service.cadastrar("Romance", "Livros de romance")

print("Criando autores de exemplo...")
autor_herbert = autor_service.cadastrar("Frank Herbert", "Norte-americano")
autor_machado = autor_service.cadastrar("Machado de Assis", "Brasileiro")

print("Criando editoras de exemplo...")
editora_aleph = editora_service.cadastrar("Aleph", "São Paulo")
editora_penguin = editora_service.cadastrar("Penguin", "São Paulo")

print("Criando livros de exemplo...")
livro_service.cadastrar("Duna", "978-85-01", cat_ficcao.id, autor_herbert.id, editora_aleph.id, qtd_total=2)
livro_service.cadastrar("Dom Casmurro", "978-85-02", cat_romance.id, autor_machado.id, editora_penguin.id, qtd_total=1)

print("\nDados de exemplo criados com sucesso!")
print("Login admin -> email: admin@biblioteca.com  | senha: admin123")
print("Login leitor -> email: maria@email.com       | senha: leitor123")
