from datetime import datetime
from model.pessoa import Pessoa
from utils.validadores.validar_pessoa_fisica import ValidarPessoaFisica as Validar


class PessoaFisica(Pessoa):
    """
    Representa uma pessoa física com CPF e data de nascimento.
    Herda os campos comuns da classe Pessoa.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        numero_documento: str,
        cep: str,
        numero_endereco: str,
        endereco: str,
        telefone: str,
        data_nascimento: str | datetime
    ):
        """
        Inicializa uma Pessoa Física com dados pessoais e data de nascimento.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Endereço de e-mail.
            numero_documento (str): CPF da pessoa (11 dígitos).
            cep (str): CEP do endereço.
            numero_endereco (str): Número da residência.
            endereco (str): Endereço completo.
            telefone (str): Telefone da pessoa.
            data_nascimento (str | datetime): Data de nascimento (formato 'dd/mm/aaaa' ou datetime).
        """
        # Validação completa dos dados
        erros = Validar.todos_campos(
            nome, email, numero_documento, cep, numero_endereco, telefone, data_nascimento
        )
        if erros:
            raise ValueError("\n".join(erros))

        # Inicialização dos atributos comuns herdados
        super().__init__(nome, email, numero_documento, cep, numero_endereco, telefone)

        # Conversão da data de nascimento se for string
        self._data_nascimento = (
            datetime.strptime(data_nascimento, "%d/%m/%Y")
            if isinstance(data_nascimento, str)
            else data_nascimento
        )

    def __str__(self) -> str:
        return f"{self._nome} (CPF: {self._numero_documento})"

    def get_data_nascimento(self) -> datetime:
        """
        Retorna a data de nascimento como objeto datetime.

        Returns:
            datetime: Data de nascimento.
        """
        return self._data_nascimento

    def get_tipo(self) -> str:
        """
        Retorna o tipo da pessoa ('fisica').

        Returns:
            str: Tipo da pessoa.
        """
        return "fisica"