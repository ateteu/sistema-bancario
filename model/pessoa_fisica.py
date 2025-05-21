from utils import validadores
from model.pessoa import Pessoa

class PessoaFisica(Pessoa):
    
    def __str__(self) -> str:
        """
        Retorna uma representação textual simples da pessoa física.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._cpf})"
