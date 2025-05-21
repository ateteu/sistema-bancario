from typing import List
from model.pessoa import Pessoa
from model.conta import Conta

class Cliente:
    """
    Representa um cliente do sistema bancário.

    Attributes:
        _pessoa (Pessoa): Objeto que representa os dados pessoais do cliente.
        _senha (str): Senha de acesso do cliente ao sistema.
        _contas (List[Conta]): Lista de contas associadas ao cliente.
    """

    def __init__(self, pessoa: Pessoa, senha: str, contas: List[Conta] = None) -> None:
        """
        Inicializa um novo cliente com os dados fornecidos.

        Args:
            pessoa (Pessoa): Objeto Pessoa contendo os dados do cliente.
            senha (str): Senha de acesso do cliente.
            contas (List[Conta], optional): Lista inicial de contas do cliente. Defaults to None.
        """
        self._pessoa = pessoa
        self._senha = senha
        self._contas = contas if contas is not None else []

    @property
    def pessoa(self) -> Pessoa:
        """
        Retorna o objeto Pessoa associado ao cliente.

        Returns:
            Pessoa: Objeto Pessoa do cliente.
        """
        return self._pessoa

    @property
    def contas(self) -> List[Conta]:
        """
        Retorna a lista de contas associadas ao cliente.

        Returns:
            List[Conta]: Lista de contas do cliente.
        """
        return self._contas

    def verificar_senha(self, senha_digitada: str) -> bool:
        """
        Verifica se a senha informada está correta.

        Args:
            senha_digitada (str): Senha digitada para verificação.

        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        return self._senha == senha_digitada

    def set_senha(self, senha_antiga: str, nova_senha: str) -> bool:
        """
        Altera a senha do cliente se a senha antiga estiver correta.

        Args:
            senha_antiga (str): Senha atual.
            nova_senha (str): Nova senha desejada.

        Returns:
            bool: True se a alteração foi realizada com sucesso, False caso contrário.

        Raises:
            ValueError: Se a nova senha não for válida.
        """
        if self.verificar_senha(senha_antiga):
            self._senha = nova_senha
            return True
        return False
