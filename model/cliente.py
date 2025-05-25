from typing import List
from model.pessoa import Pessoa
from model.conta import Conta
from utils.validadores.validar_cliente import ValidarCliente as Validar

class Cliente:
    """
    Representa um cliente do sistema bancário, ou seja, uma Pessoa, 
    com uma senha de acesso ao sistema e que pode ou não ter contas associadas.

    Attributes:
        _pessoa (Pessoa): Objeto que representa os dados pessoais do cliente.
        _senha (str): Senha de acesso do cliente ao sistema.
        _contas (List[Conta]): Lista de contas associadas ao cliente.
    """

    def __init__(self, pessoa: Pessoa, senha: str, contas: List[Conta] = None) -> None:
        """
        Inicializa um novo cliente com os dados fornecidos.
        Obs: A senha não é validada nesse construtor!

        Args:
            pessoa (Pessoa): Objeto Pessoa contendo os dados do cliente.
            senha (str): Senha de acesso do cliente.
            contas (List[Conta], optional): Lista inicial de contas associadas ao cliente. 
                Caso não seja fornecida, será considerada uma lista vazia.

        Raises:
            TypeError: Se 'pessoa' não for uma instância de Pessoa.
            TypeError: Se algum item de 'contas' não for uma instância de Conta.
        """
        if not isinstance(pessoa, Pessoa):
            raise TypeError("O parâmetro 'pessoa' deve ser um objeto da classe Pessoa.")
        
        if contas is None:
            contas = []
        elif not all(isinstance(c, Conta) for c in contas):
            raise TypeError("Todos os itens em 'contas' devem ser objetos da classe Conta.")
        
        self._pessoa = pessoa
        self._senha  = senha
        self._contas = contas

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
            bool: True se a senha digitada estiver correta, False caso contrário.
        """
        return self._senha == senha_digitada

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> None:
        """
        Altera a senha do cliente se a senha antiga estiver correta.

        Args:
            senha_atual (str): Senha atual.
            nova_senha (str): Nova senha desejada.

        Raises:
            ValueError: Se a senha atual estiver incorreta ou a nova senha pretendida for inválida.
        """
        if not self.verificar_senha(senha_atual):
            raise ValueError("Senha atual incorreta. Por favor, verifique se foi digitada corretamente.")
        
        Validar.senha(nova_senha) # Valida força da nova senha
        self._senha = nova_senha

    def possui_conta(self) -> bool:
        """
        Verifica se o cliente possui uma ou mais contas associadas.

        Returns:
            bool: True se possuir pelo menos uma conta, False caso contrário.
        """
        return bool(self._contas)
    