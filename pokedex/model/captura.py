class Captura:
    """Entidade Captura - associa um Usuario (treinador) a um Pokemon (N para 1 em ambos)."""

    STATUS_ATIVO = "ATIVO"
    STATUS_LIBERTADO = "LIBERTADO"

    def __init__(self, pokemon_id, treinador_id, apelido, data_captura,
                 id=None, data_libertacao=None, status=None):
        self.id = id
        self.pokemon_id = pokemon_id
        self.treinador_id = treinador_id
        self.apelido = apelido
        self.data_captura = data_captura
        self.data_libertacao = data_libertacao
        self.status = status if status else Captura.STATUS_ATIVO

    def to_dict(self):
        return {
            "id": self.id,
            "pokemon_id": self.pokemon_id,
            "treinador_id": self.treinador_id,
            "apelido": self.apelido,
            "data_captura": self.data_captura,
            "data_libertacao": self.data_libertacao,
            "status": self.status,
        }

    @staticmethod
    def from_dict(d):
        return Captura(
            pokemon_id=d["pokemon_id"],
            treinador_id=d["treinador_id"],
            apelido=d["apelido"],
            data_captura=d["data_captura"],
            id=d.get("id"),
            data_libertacao=d.get("data_libertacao"),
            status=d.get("status"),
        )

    def __repr__(self):
        return (f"Captura(id={self.id}, pokemon_id={self.pokemon_id}, "
                f"treinador_id={self.treinador_id}, apelido='{self.apelido}', status='{self.status}')")
