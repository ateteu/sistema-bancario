from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores import validar_data_nascimento

class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com data de nascimento e representação textual por CPF.
    """
    def __init__(self, nome: str, email: str, numero_documento: str, cep: str, numero_endereco: str, endereco: str, data_nascimento: str):
        """
        Inicializa uma pessoa física.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Email da pessoa.
            numero_documento (str): Número de documento da pessoa (único e imutável).
            cep (str): CEP da residência.
            numero_endereco (str): Número do endereço.
            endereco (str): Endereço completo (resolvido a partir do CEP e número).
            data_nascimento (str): Data de nascimento no formato "dd/mm/aaaa".
        """
        super().__init__(numero_documento, nome, email, cep, numero_endereco, endereco)
        self._data_nascimento = data_nascimento

    def __str__(self) -> str:
        """
        Retorna uma representação textual simples da pessoa física.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._cpf})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento da pessoa física.

        Returns:
            datetime: Data de nascimento da pessoa.
        """
        return self._data_nascimento

    def set_data_nascimento(self, data_nascimento: datetime) -> None:
            """
            Define a data de nascimento da pessoa física, após validação.

            Args:
                data_nascimento (datetime): Data de nascimento a ser atribuída.

            Raises:
                ValueError: Se a data for inválida.
            """
            validar_data_nascimento(data_nascimento)
            self._data_nascimento = data_nascimento
