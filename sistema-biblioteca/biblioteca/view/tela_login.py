from service.usuario_service import UsuarioService
from model.usuario import Usuario
from view.menu_administrador import menu_administrador
from view.menu_leitor import menu_leitor


def tela_login():
    usuario_service = UsuarioService()
    print("======================================")
    print(" SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
    print("======================================")
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    usuario = usuario_service.autenticar(email, senha)
    if not usuario:
        print("Credenciais inválidas.")
        return

    print(f"\nBem-vindo(a), {usuario.nome}! Perfil: {usuario.perfil}")

    # Implementação de menu de operações de acordo com o perfil do usuário
    if usuario.perfil == Usuario.PERFIL_ADMIN:
        menu_administrador(usuario)
    elif usuario.perfil == Usuario.PERFIL_LEITOR:
        menu_leitor(usuario)
    else:
        print("Perfil não reconhecido.")


if __name__ == "__main__":
    tela_login()
