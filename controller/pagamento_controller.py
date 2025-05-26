from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.exceptions import ContaInativaError


class PagamentoController:
    """
    Controlador responsável por realizar transferências entre contas de clientes.
    """

    @staticmethod
    def realizar_pagamento(dados: dict, banco=None) -> dict:
        """
        Executa uma transferência entre contas bancárias.

        Args:
            dados (dict): Dicionário com os seguintes campos:
                - conta_origem (str): Número da conta de origem.
                - cpf_destino (str): CPF do cliente destinatário.
                - valor (float): Valor a ser transferido.
                - descricao (str): Descrição da transação (opcional).

            banco (opcional): Argumento mantido por compatibilidade, atualmente não utilizado.

        Returns:
            dict: Resultado da operação com status ('sucesso': bool) e mensagem/erros.
        """
        # Validação de entrada básica
        conta_origem_num = str(dados.get("conta_origem"))
        cpf_destino = dados.get("cpf_destino", "").strip()
        valor = dados.get("valor")

        if not conta_origem_num or not cpf_destino or valor is None:
            return {"sucesso": False, "erros": ["Dados obrigatórios ausentes."]}

        if not isinstance(valor, (int, float)) or valor <= 0:
            return {"sucesso": False, "erros": ["Valor inválido para transferência."]}

        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        # Busca destinatário e valida conta ativa
        cliente_destino = cliente_dao.buscar_por_id(cpf_destino)
        if not cliente_destino:
            return {"sucesso": False, "erros": [f"Destinatário com CPF {cpf_destino} não encontrado."]}

        conta_destino = next((c for c in cliente_destino.contas if c.get_estado_da_conta()), None)
        if not conta_destino:
            return {"sucesso": False, "erros": ["Destinatário não possui conta ativa."]}

        # Busca conta de origem
        conta_origem = conta_dao.buscar_por_id(conta_origem_num)
        if not conta_origem:
            return {"sucesso": False, "erros": ["Conta de origem não encontrada."]}

        if conta_destino.get_numero_conta() == conta_origem.get_numero_conta():
            return {"sucesso": False, "erros": ["Não é possível transferir para a mesma conta."]}

        # Realiza a transferência com tratamento de exceções
        try:
            conta_origem.transferir(conta_destino, valor)
        except ContaInativaError as e:
            return {"sucesso": False, "erros": [str(e)]}
        except ValueError as e:
            return {"sucesso": False, "erros": [str(e)]}
        except Exception:
            return {"sucesso": False, "erros": ["Erro inesperado ao realizar a transferência."]}

        # Atualiza estado das contas no sistema
        conta_dao.atualizar_objeto(conta_origem)
        conta_dao.atualizar_objeto(conta_destino)

        mensagem = f"Transferência de R$ {valor:.2f} realizada com sucesso para {cpf_destino}."
        return {"sucesso": True, "mensagem": mensagem}