class Emprestimo:
    """Entidade Emprestimo - associa um Usuario (leitor) a um Livro (N para 1 em ambos)."""

    STATUS_ATIVO = "ATIVO"
    STATUS_DEVOLVIDO = "DEVOLVIDO"

    def __init__(self, livro_id, usuario_id, data_emprestimo, data_devolucao_prevista,
                 id=None, data_devolucao_real=None, status=None):
        self.id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista
        self.data_devolucao_real = data_devolucao_real
        self.status = status if status else Emprestimo.STATUS_ATIVO

    def to_dict(self):
        return {
            "id": self.id,
            "livro_id": self.livro_id,
            "usuario_id": self.usuario_id,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao_prevista": self.data_devolucao_prevista,
            "data_devolucao_real": self.data_devolucao_real,
            "status": self.status,
        }

    @staticmethod
    def from_dict(d):
        return Emprestimo(
            livro_id=d["livro_id"],
            usuario_id=d["usuario_id"],
            data_emprestimo=d["data_emprestimo"],
            data_devolucao_prevista=d["data_devolucao_prevista"],
            id=d.get("id"),
            data_devolucao_real=d.get("data_devolucao_real"),
            status=d.get("status"),
        )

    def __repr__(self):
        return (f"Emprestimo(id={self.id}, livro_id={self.livro_id}, "
                f"usuario_id={self.usuario_id}, status='{self.status}')")
