import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dados.banco import Banco
from modelos.usuario import Cliente

class ManterClienteUI:
    def __init__(self):
        self.banco = Banco()

    def main(self):
        st.header("Cadastro de Clientes")
        aba = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with aba[0]:
            self.listar()
        with aba[1]:
            self.inserir()
        with aba[2]:
            self.atualizar()
        with aba[3]:
            self.excluir()

    def listar(self):
        clientes = [
            {"_id": u.login, "_nome": u.nome, "_email": u.email, "_fone": u.telefone}
            for u in self.banco.usuarios.values()
            if isinstance(u, Cliente)
        ]
        st.dataframe(clientes)

    def inserir(self):
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        fone = st.text_input("Informe o fone")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Inserir"):
            if nome and email and fone and senha:
                login = email
                if login in self.banco.usuarios:
                    st.error("Esse e-mail ja esta cadastrado.")
                else:
                    novo = Cliente(
                        login=login,
                        senha=senha,
                        nome=nome,
                        email=email,
                        telefone=fone,
                        cpf="",
                        endereco=""
                    )
                    self.banco.usuarios[login] = novo
                    st.success("Cliente inserido com sucesso!")
            else:
                st.warning("Preencha todos os campos.")

    def atualizar(self):
        clientes = [u for u in self.banco.usuarios.values() if isinstance(u, Cliente)]

        if len(clientes) == 0:
            st.info("Nenhum cliente cadastrado.")
            return

        opcoes = [f"{u.login} - {u.nome} - {u.email} - {u.telefone}" for u in clientes]
        selecionado = st.selectbox("Atualizacao de Clientes", opcoes)

        login = selecionado.split(" - ")[0]
        cliente = self.banco.usuarios.get(login)

        novo_nome = st.text_input("Informe o novo nome", value=cliente.nome)
        novo_email = st.text_input("Informe o novo e-mail", value=cliente.email)
        novo_fone = st.text_input("Informe o novo fone", value=cliente.telefone)
        nova_senha = st.text_input("Informe a nova senha", value=cliente.senha, type="password")

        if st.button("Atualizar"):
            cliente.nome = novo_nome
            cliente.email = novo_email
            cliente.telefone = novo_fone
            cliente.senha = nova_senha
            st.success("Cliente atualizado com sucesso!")

    def excluir(self):
        clientes = [u for u in self.banco.usuarios.values() if isinstance(u, Cliente)]

        if len(clientes) == 0:
            st.info("Nenhum cliente cadastrado.")
            return

        opcoes = [f"{u.login} - {u.nome} - {u.email} - {u.telefone}" for u in clientes]
        selecionado = st.selectbox("Exclusao de Clientes", opcoes)

        if st.button("Excluir"):
            login = selecionado.split(" - ")[0]
            del self.banco.usuarios[login]
            st.success("Cliente excluido com sucesso!")