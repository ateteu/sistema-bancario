from abc import ABC, abstractmethod
from utils.validadores.validar_pessoa import ValidarPessoa as Validar
from utils.api import API

class Pessoa(ABC):
    """
    Representa uma pessoa.

    Attributes:
        _nome (str): Nome completo da pessoa.
        _email (str): Email da pessoa.
        _numero_documento (str): Número de documento da pessoa (único e imutável).
        _cep (str): CEP da residência da pessoa.
        _numero_endereco (str): Número do endereço da pessoa.
        _endereco (str): Endereço completo da pessoa (obtido pela API viaCEP).
        _telefone (str): Telefone da pessoa.
    """

    def __init__(self, nome: str, email: str, numero_documento: str, cep: str, numero_endereco: str, telefone: str) -> None:
        """
        Inicializa uma instância de Pessoa com os dados fornecidos.

        Atenção:
            Esta classe é abstrata e não deve ser instanciada diretamente.
            Espera-se que os dados fornecidos já estejam validados pelas subclasses
            antes de serem passados para este construtor.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Email da pessoa.
            numero_documento (str): Número de documento da pessoa (único e imutável).
            cep (str): CEP da residência.
            numero_endereco (str): Número do endereço.
            telefone (str): Telefone da pessoa.
        
        Raises:
            ValueError: Caso haja erro ao atualizar o endereço via API (viaCEP).
        """
        self._nome             = nome
        self._email            = email
        self._numero_documento = numero_documento
        self._cep              = cep
        self._numero_endereco  = numero_endereco
        self._telefone         = telefone

        self._atualizar_endereco()

    @abstractmethod
    def __str__(self) -> str:
        """
        Representação textual da pessoa.
        Deve ser implementado nas subclasses.
        """
        pass

    def get_nome(self) -> str:
        """
        Retorna o nome da pessoa.

        Returns:
            str: Nome da pessoa.
        """
        return self._nome

    def set_nome(self, novo_nome: str) -> None:
        """
        Altera o nome da pessoa.

        Args:
            novo_nome (str): Novo nome a ser atribuído.
        
        Raises:
            ValueError: Se o nome for inválido.
        """
        Validar.nome(novo_nome)
        self._nome = novo_nome

    def get_email(self) -> str:
        """
        Retorna o e-mail da pessoa.

        Returns:
            str: Email da pessoa.
        """
        return self._email

    def set_email(self, novo_email: str) -> None:
        """
        Altera o e-mail da pessoa.
        
        Args:
            novo_email (str): Novo email a ser atribuído.
        
        Raises:
            ValueError: Se o e-mail for inválido.
        """
        Validar.email(novo_email)
        self._email = novo_email

    def get_numero_documento(self) -> str:
        """
        Retorna o número de documento da pessoa (CPF/CNPJ).

        Returns:
            str: Número de documento da pessoa.
        """
        return self._numero_documento

    def get_cep(self) -> str:
        """
        Retorna o CEP da residência da pessoa.

        Returns:
            str: CEP atual.
        """
        return self._cep

    def set_cep(self, novo_cep: str) -> None:
        """
        Altera o CEP da residência da pessoa.

        Args:
            novo_cep (str): Novo CEP a ser atribuído.
        
        Raises:
            ValueError: Se o CEP for inválido.
        """
        Validar.cep(novo_cep)
        self._cep = novo_cep

    def get_numero_endereco(self) -> str:
        """
        Retorna o Número do endereço da pessoa.

        Returns:
            str: Número do endereço.
        """
        return self._numero_endereco

    def set_numero_endereco(self, novo_numero: str) -> None:
        """
        Altera o Número do endereço da pessoa.

        Args:
            novo_numero (str): Novo Número do endereço.
        
        Raises:
            ValueError: Se o Número do endereço for inválido.
        """
        Validar.numero_endereco(novo_numero)
        self._numero_endereco = novo_numero

    def get_endereco(self) -> str:
        """
        Retorna o endereço completo da pessoa.

        Returns:
            str: Endereço completo.
        """
        return self._endereco

    def _atualizar_endereco(self) -> None:
        """
        Atualiza o atributo de endereço com base no CEP e número do endereço da instância.

        Realiza uma consulta à API ViaCEP utilizando o CEP e o número do imóvel já definidos
        para obter e atualizar o endereço completo no formato adequado.

        Raises:
            ValueError: Se o CEP for inválido ou não encontrado.
            ValueError: Se o número do endereço for inválido.
            ValueError: Se houver erro na consulta.
        """
        self._endereco = API.buscar_endereco_por_cep(self._cep, self._numero_endereco)

    def get_telefone(self) -> str:
        """
        Retorna o número de telefone da pessoa.

        Returns:
            str: Número de telefone.
        """
        return self._telefone

    def set_telefone(self, novo_telefone: str) -> None:
        """
        Altera o número de telefone da pessoa.

        Args:
            novo_telefone (str): Novo número de telefone a ser atribuído.

        Raises:
            ValueError: Se o número de telefone for inválido.
        """
        Validar.telefone(novo_telefone)
        self._telefone = novo_telefone
