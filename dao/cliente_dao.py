from typing import Optional, List
from model.cliente import Cliente
from dao.dao import DAO
from dao.pessoa_dao import PessoaDAO
from dao.conta_dao import ContaDAO
from utils.constantes import ARQUIVO_CLIENTES

class ClienteDAO(DAO):
    """
    DAO para persistência de Clientes no arquivo correspondente.
    """

    def __init__(self):
        """
        Inicializa o DAO de clientes e os DAOs auxiliares de pessoas e contas.
        """
        super().__init__(ARQUIVO_CLIENTES)
        self._pessoa_dao = PessoaDAO()
        self._conta_dao = ContaDAO()
        self._cache_clientes_objetos = None  # Cache dos clientes reconstruídos

    def criar_objeto(self, dados: dict) -> Cliente:
        """
        Cria uma instância de Cliente, usando dados passados, carregando Pessoa e Contas.
        """
        pessoa = self._pessoa_dao.buscar_por_id(dados["numero_documento"])
        todas_contas = {c.get_numero_conta(): c for c in self._conta_dao.listar_todos_objetos()}

        contas = []
        for n in dados.get("contas", []):
            try:
                numero = int(n)
                if numero in todas_contas:
                    contas.append(todas_contas[numero])
            except ValueError:
                continue

        return Cliente(pessoa=pessoa, senha=dados["senha"], contas=contas)

    def extrair_dados_do_objeto(self, obj: Cliente) -> dict:
        return {
            "numero_documento": obj.pessoa.get_numero_documento(),
            "senha": obj._senha,
            "contas": [str(c.get_numero_conta()) for c in obj.contas],
        }

    def tipo_de_id(self) -> str:
        return "numero_documento"

    def buscar_por_id(self, id_valor: str) -> Optional[Cliente]:
        return super().buscar_por_id(id_valor)

    def listar_todos_objetos(self) -> List[Cliente]:
        if self._cache_clientes_objetos is not None:
            return self._cache_clientes_objetos

        dados_raw = self._ler_dados_do_json()
        self._cache_clientes_objetos = [self.criar_objeto(d) for d in dados_raw]
        return self._cache_clientes_objetos

    def salvar_objeto(self, obj: Cliente) -> None:
        super().salvar_objeto(obj)
        self._cache_clientes_objetos = None

    def atualizar_objeto(self, obj: Cliente) -> bool:
        resultado = super().atualizar_objeto(obj)
        self._cache_clientes_objetos = None
        return resultado

    def deletar_objeto(self, id_valor: str) -> bool:
        resultado = super().deletar_objeto(id_valor)
        self._cache_clientes_objetos = None
        return resultado

    def buscar_cliente_por_numero_conta(self, numero_conta: int) -> Optional[Cliente]:
        print(f"🔍 [DEBUG] Procurando cliente que possui a conta: {numero_conta}")
        clientes = self.listar_todos_objetos()
        print(f"🔍 [DEBUG] Total de clientes carregados: {len(clientes)}")

        for cliente in clientes:
            print(f"👤 [DEBUG] Verificando cliente: {cliente.pessoa.get_nome()}")
            for conta in cliente.contas:
                print(f"   ↳ [DEBUG] Conta do cliente: {conta.get_numero_conta()} (tipo: {type(conta.get_numero_conta())})")
                if str(conta.get_numero_conta()) == str(numero_conta):
                    print("✅ [DEBUG] Cliente encontrado!")
                    return cliente

        print("❌ [DEBUG] Nenhum cliente encontrado com essa conta.")
        return None
