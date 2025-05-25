from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_fisica import ValidarPessoaFisica as Validar

class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física, com data de nascimento e representação textual por CPF.
    """

    def __init__(self, nome: str, email: str, cpf: str, cep: str, numero_endereco: str, telefone: str, data_nascimento: str|datetime):
        """
        Inicializa uma pessoa física.
        Obs: Data de nascimento é recebido como str, mas armazenado no objeto como datetime.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Email da pessoa.
            cpf (str): Número de documento da pessoa (único e imutável).
            cep (str): CEP da residência.
            numero_endereco (str): Número do endereço.
            telefone (str): Telefone da pessoa.
            data_nascimento (str | datetime): Data de nascimento no formato "dd/mm/aaaa" se for str ou no formato datetime.

        Raises:
            ValueError: Se houver algum erro nos dados.
            ValueError: Se houver erro ao usar a API (no construtor abstrato)
        """
        erros = Validar.todos_campos(nome, email, cpf, cep, numero_endereco, telefone, data_nascimento)
        if erros:
            raise ValueError("\n".join(erros))

        super().__init__(nome, email, cpf, cep, numero_endereco, telefone)
        self._data_nascimento = data_nascimento

    def __str__(self) -> str:
        """
        Retorna uma representação textual simples da pessoa física.

        Returns:
            str: Nome e CPF formatados.
        """
        return f"{self._nome} (CPF: {self._numero_documento})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento da pessoa física.

        Returns:
            datetime: Data de nascimento da pessoa.
        """
        return self._data_nascimento
