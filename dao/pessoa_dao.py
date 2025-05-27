from dao.dao import DAO
from model.pessoa import Pessoa
from mapper.pessoa_mapper import PessoaMapper
from utils.constantes import ARQUIVO_PESSOAS

class PessoaDAO(DAO):
    """
    DAO para persistência de objetos do tipo Pessoa no arquivo correspondente.

    Esta classe é responsável por serializar e desserializar objetos Pessoa (e suas subclasses)
    para armazenamento e leitura em formato JSON.
    """

    def __init__(self):
        """
        Inicializa o DAO de pessoas com o caminho do arquivo JSON.
        """
        super().__init__(ARQUIVO_PESSOAS)
        self._cache_pessoas = None  # ✅ cache em memória

    def criar_objeto(self, dados: dict) -> Pessoa:
        """
        Constrói um objeto Pessoa (ou subclasse) a partir de um dicionário.
        """
        return PessoaMapper.from_dict(dados)

    def extrair_dados_do_objeto(self, pessoa: Pessoa) -> dict:
        """
        Converte um objeto Pessoa (ou subclasse) em um dicionário serializável.
        """
        return PessoaMapper.to_dict(pessoa)

    def tipo_de_id(self) -> str:
        """
        Retorna o nome do campo usado como identificador único da pessoa.
        """
        return "numero_documento"

    def listar_todos_objetos(self) -> list[Pessoa]:
        """
        Retorna todas as pessoas, utilizando cache para evitar reconstrução.
        """
        if self._cache_pessoas is not None:
            return self._cache_pessoas

        dados = self._ler_dados_do_json()
        self._cache_pessoas = [self.criar_objeto(d) for d in dados]
        return self._cache_pessoas

    def buscar_por_id(self, id_valor: str) -> Pessoa | None:
        """
        Busca uma pessoa por documento, utilizando cache.
        """
        for pessoa in self.listar_todos_objetos():
            if str(pessoa.get_numero_documento()) == str(id_valor):
                return pessoa
        return None

    def salvar_objeto(self, pessoa: Pessoa) -> None:
        super().salvar_objeto(pessoa)
        self._cache_pessoas = None  # invalida cache ao salvar

    def atualizar_objeto(self, pessoa: Pessoa) -> bool:
        atualizado = super().atualizar_objeto(pessoa)
        self._cache_pessoas = None  # invalida cache ao atualizar
        return atualizado

    def deletar_objeto(self, id_valor: str) -> bool:
        deletado = super().deletar_objeto(id_valor)
        self._cache_pessoas = None  # invalida cache ao deletar
        return deletado
