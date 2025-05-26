from abc import ABC, abstractmethod
from utils.validadores.validar_pessoa import ValidarPessoa as Validar
from utils.api import API


class Pessoa(ABC):
    """
    Classe abstrata que representa uma pessoa (física ou jurídica).
    Deve ser estendida por subclasses especializadas.

    Atributos comuns:
        - nome, email, documento, endereço, telefone.
        - O endereço completo é obtido via API a partir do CEP e número.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        numero_documento: str,
        cep: str,
        numero_endereco: str,
        telefone: str
    ) -> None:
        """
        Inicializa uma instância de Pessoa.

        OBS: Validações devem ser feitas nas subclasses. Esta classe espera dados válidos.

        Args:
            nome (str): Nome completo da pessoa.
            email (str): Email da pessoa.
            numero_documento (str): CPF ou CNPJ da pessoa.
            cep (str): CEP da residência.
            numero_endereco (str): Número do endereço.
            telefone (str): Telefone da pessoa.

        Raises:
            ValueError: Em caso de falha ao buscar o endereço via API.
        """
        self._nome = nome
        self._email = email
        self._numero_documento = numero_documento
        self._cep = cep
        self._numero_endereco = numero_endereco
        self._telefone = telefone

        self._atualizar_endereco()

    @abstractmethod
    def __str__(self) -> str:
        """
        Retorna a representação textual da pessoa.
        Deve ser implementado pelas subclasses.
        """
        pass

    # === Getters e Setters ===

    def get_nome(self) -> str:
        return self._nome

    def set_nome(self, novo_nome: str) -> None:
        Validar.nome(novo_nome)
        self._nome = novo_nome

    def get_email(self) -> str:
        return self._email

    def set_email(self, novo_email: str) -> None:
        Validar.email(novo_email)
        self._email = novo_email

    def get_numero_documento(self) -> str:
        return self._numero_documento

    def get_cep(self) -> str:
        return self._cep

    def set_cep(self, novo_cep: str) -> None:
        Validar.cep(novo_cep)
        self._cep = novo_cep

    def get_numero_endereco(self) -> str:
        return self._numero_endereco

    def set_numero_endereco(self, novo_numero: str) -> None:
        Validar.numero_endereco(novo_numero)
        self._numero_endereco = novo_numero

    def get_endereco(self) -> str:
        return self._endereco

    def get_telefone(self) -> str:
        return self._telefone

    def set_telefone(self, novo_telefone: str) -> None:
        Validar.telefone(novo_telefone)
        self._telefone = novo_telefone

    # === Métodos auxiliares ===

    def _atualizar_endereco(self) -> None:
        """
        Atualiza o endereço completo com base no CEP e número.
        Utiliza API externa (ViaCEP).

        Raises:
            ValueError: Em caso de falha na consulta do endereço.
        """
        if hasattr(self, "_endereco_resolvido") and self._endereco_resolvido:
            return

        from time import time
        inicio = time()
        self._endereco = API.buscar_endereco_por_cep(self._cep, self._numero_endereco)
        self._endereco_resolvido = True
