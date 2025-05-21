from model.pessoa import Pessoa
from model.conta import Conta
from utils import validadores

class Cliente:
    def __init__(self, pessoa: Pessoa, senha: str, conta: Conta):
        self._pessoa = pessoa
        self._senha = senha
        self._conta = conta

    def verificar_senha(self, senha_digitada: str) -> bool:
        """
        Verifica se a senha informada é correta.

        Args:
            senha_digitada (str): Senha digitada para verificação.

        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        return self._senha == senha_digitada

    def set_senha(self, senha_antiga: str, nova_senha: str) -> bool:
        """
        Altera a senha se a senha antiga estiver correta.

        Args:
            senha_antiga (str): Senha atual.
            nova_senha (str): Nova senha desejada.

        Returns:
            bool: True se a alteração foi feita, False caso contrário.
        
        Raises:
            ValueError: Se a nova senha não for válida.
        """
        if self.verificar_senha(senha_antiga):
            validadores.validar_senha(nova_senha)
            self._senha = nova_senha
            return True
        return False
