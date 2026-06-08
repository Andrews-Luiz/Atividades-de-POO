import streamlit as st
from manter_cliente_ui import ManterClienteUI

class IndexUI:
    @staticmethod
    def main():
        manter_cliente = ManterClienteUI()
        manter_cliente.main()

if __name__ == "__main__":
    IndexUI.main()