from model.conta import Conta
from mapper.conta_mapper import ContaMapper
from dao.dao import DAO
from utils.constantes import ARQUIVO_CONTAS

class ContaDAO(DAO):
    """
    DAO responsável pela persistência de objetos do tipo Conta
    (ContaCorrente, ContaPoupanca) no arquivo em questão.
    """

    def __init__(self):
        """
        Inicializa o DAO de contas com o caminho do arquivo.
        """
        super().__init__(ARQUIVO_CONTAS)
        self._cache_contas = None  # ✅ cache local de objetos Conta

    def criar_objeto(self, dados: dict) -> Conta:
        """
        Cria uma instância de Conta a partir de um dicionário, usando o mapper de conta.
        """
        return ContaMapper.from_dict(dados)

    def extrair_dados_do_objeto(self, conta: Conta) -> dict:
        """
        Converte uma instância de Conta em dicionário, usando o mapper de conta.
        """
        return ContaMapper.to_dict(conta)

    def tipo_de_id(self) -> str:
        """
        Retorna o campo usado como identificador da conta no JSON.
        """
        return "numero"

    def listar_todos_objetos(self) -> list[Conta]:
        """
        Lista todas as contas persistidas, utilizando cache para evitar reprocessamento.
        """
        if self._cache_contas is not None:
            return self._cache_contas

        dados = self._ler_dados_do_json()
        self._cache_contas = [self.criar_objeto(d) for d in dados]
        return self._cache_contas

    def buscar_por_id(self, id_valor: str) -> Conta | None:
        """
        Busca uma conta pelo número, utilizando cache local.
        """
        for conta in self.listar_todos_objetos():
            if str(conta.get_numero_conta()) == str(id_valor):
                return conta
        return None

    def salvar_objeto(self, conta: Conta) -> None:
        super().salvar_objeto(conta)
        self._cache_contas = None  # ❌ invalida cache após salvar

    def atualizar_objeto(self, conta: Conta) -> bool:
        atualizado = super().atualizar_objeto(conta)
        self._cache_contas = None
        return atualizado

    def deletar_objeto(self, id_valor: str) -> bool:
        deletado = super().deletar_objeto(id_valor)
        self._cache_contas = None
        return deletado
