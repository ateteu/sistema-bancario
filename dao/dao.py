from abc import ABC, abstractmethod
import json
import os
from typing import List, Optional, TypeVar, Generic
T = TypeVar("T") # Tipo genérico para entidades do DAO

class DAO(ABC, Generic[T]):
    """
    Classe base abstrata para DAOs que lidam com persistência em arquivos JSON.
    """

    def __init__(self, arquivo_json: str):
        """
        Inicializa um objeto de acesso genérico.

        Args:
            arquivo_json (str): Caminho do arquivo JSON para armazenar os dados.
        """
        self.arquivo_json = os.path.join("database", arquivo_json)

    @abstractmethod
    def criar_objeto(self, data: dict):
        """
        Converte um dicionário para um objeto da entidade.

        Args:
            data (dict): Dicionário com dados da entidade.

        Returns:
            Objeto da entidade correspondente.
        """
        pass

    @abstractmethod
    def extrair_dados_do_objeto(self, obj) -> dict:
        """
        Extrai informações de um objeto da entidade, formando um dicionário.

        Args:
            obj: Objeto da entidade.

        Returns:
            dict: Dicionário com dados para salvar no JSON.
        """
        pass

    @abstractmethod
    def tipo_de_id(self) -> str:
        """
        Retorna o nome do campo usado como identificador único no JSON.

        Returns:
            str: Nome do campo identificador único.
        """
        pass

    def _ler_dados_do_json(self) -> List[dict]:
        """
        Carrega os dados do arquivo JSON.

        Returns:
            List[dict]: Lista de dicionários representando as entidades.

        Nota:
            Retorna lista vazia se o arquivo não existir ou estiver vazio/corrompido.
        """
        try:
            with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _salvar_no_arquivo_json(self, dados: List[dict]) -> None:
        """
        Salva os dados no arquivo JSON.

        Args:
            dados (List[dict]): Lista de dicionários para salvar.
        """
        with open(self.arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)

    def listar_todos_objetos(self) -> List[T]:
        """
        Retorna todos os objetos da entidade armazenados.

        Returns:
            List: Lista de objetos da entidade.
        """
        dados = self._ler_dados_do_json()
        return [self.criar_objeto(item) for item in dados]

    def buscar_por_id(self, id_valor) -> Optional[T]:
        """
        Busca um objeto da entidade pelo seu identificador único.

        Args:
            id_valor: Valor do identificador único.

        Returns:
            Objeto da entidade se encontrado, None caso contrário.
        """
        dados = self._ler_dados_do_json()
        print(f"\n🔎 [DEBUG] DAO.buscar_por_id()")
        print(f"   ➤ Procurando por id = {id_valor} (tipo: {type(id_valor)})")
        print(f"   ➤ Tipo de ID definido pela entidade: {self.tipo_de_id()}")
        print(f"   📁 Total de registros carregados: {len(dados)}")

        for item in dados:
            valor_item = item.get(self.tipo_de_id())
            print(f"     ↳ Comparando com item[{self.tipo_de_id()}] = {valor_item} (tipo: {type(valor_item)})")
            if str(valor_item) == str(id_valor):  # ✅ correção aqui
                print("   ✅ Objeto encontrado!\n")
                return self.criar_objeto(item)


        print("   ❌ Nenhum objeto encontrado com este ID.\n")
        return None

    def salvar_objeto(self, obj: T) -> None:
        dados = self._ler_dados_do_json()
        novo = self.extrair_dados_do_objeto(obj)
        chave = self.tipo_de_id()

        print(">>> Tentando salvar objeto:", novo)

        if any(item.get(chave) == novo[chave] for item in dados):
            raise ValueError(f"Objeto com {chave} = '{novo[chave]}' já existe.")

        dados.append(novo)
        self._salvar_no_arquivo_json(dados)
        print(">>> Objeto salvo com sucesso.")



    def atualizar_objeto(self, obj) -> bool:
        """
        Atualiza um objeto existente no armazenamento.

        Args:
            obj: Objeto da entidade com dados atualizados.

        Returns:
            bool: True se atualização foi realizada, False se objeto não encontrado.
        """
        dados = self._ler_dados_do_json()
        id_chave = self.tipo_de_id()

        # ✅ Usa o dicionário extraído para pegar o ID corretamente
        novo_dado = self.extrair_dados_do_objeto(obj)
        id_valor = novo_dado[id_chave]

        for i, item in enumerate(dados):
            if item.get(id_chave) == id_valor:
                dados[i] = novo_dado
                self._salvar_no_arquivo_json(dados)
                print(f">>> Objeto com {id_chave} = {id_valor} atualizado com sucesso.")
                return True

        print(f"[ATUALIZAR] Objeto com {id_chave} = {id_valor} não encontrado.")
        return False



    def deletar_objeto(self, id_valor) -> bool:
        """
        Remove um objeto pelo identificador único.

        Args:
            id_valor: Valor do identificador único do objeto a ser removido.

        Returns:
            bool: True se remoção foi realizada, False se objeto não encontrado.
        """
        dados = self._ler_dados_do_json()
        novo_dados = [item for item in dados if item.get(self.tipo_de_id()) != id_valor]
        if len(novo_dados) == len(dados):
            return False
        self._salvar_no_arquivo_json(novo_dados)
        return True
