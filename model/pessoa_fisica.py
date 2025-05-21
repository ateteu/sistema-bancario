from utils import validadores
from model.pessoa import Pessoa

class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com representação textual por CPF.
    """

    def __str__(self) -> str:
        """
        Retorna uma representação textual simples da pessoa física.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._cpf})"
