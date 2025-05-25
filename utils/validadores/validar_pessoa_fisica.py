from datetime import datetime
from utils.validadores.validar_pessoa import ValidarPessoa
from utils.constantes import IDADE_MINIMA

class ValidarPessoaFisica(ValidarPessoa):
    """
    Classe utilitária que herda de ValidarPessoa validações básicas e 
    implementa validações específicas de pessoas físicas.
    """
    @staticmethod
    def cpf(cpf: str) -> None:
        """
        Valida se o CPF é válido no formato básico.
        Aceita strings com ou sem pontos/traços.

        Args:
            cpf (str): Número de CPF a ser validado.

        Raises:
            ValueError: Se o CPF estiver em branco ou não contiver exatamente 11 dígitos numéricos.
        """
        cpf_limpo = ValidarPessoa._limpar_numeros(cpf)

        if not cpf_limpo:
            raise ValueError("O CPF não pode estar em branco.")

        if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
    
    @staticmethod
    def data_nascimento(data: datetime, idade_minima: int = IDADE_MINIMA) -> None:
        """
        Valida uma data de nascimento.

        Verifica se a data não é futura e se a pessoa tem a idade mínima.

        Args:
            data (datetime): Data de nascimento a validar.
            idade_minima (int, opcional): Idade mínima exigida.

        Raises:
            ValueError: Se a data for no futuro ou a idade for inferior à mínima.
        """
        hoje = datetime.today()

        if data > hoje:
            raise ValueError("A data de nascimento não pode estar no futuro.")

        idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))

        if idade < idade_minima:
            raise ValueError(f"A pessoa deve ter pelo menos {idade_minima} anos.")
