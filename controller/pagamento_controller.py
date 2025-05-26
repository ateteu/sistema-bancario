from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.exceptions import ContaInativaError


class PagamentoController:
    @staticmethod
    def realizar_pagamento(dados: dict, banco=None) -> dict:
        """
        Realiza um pagamento entre contas (transferência).

        Args:
            dados (dict): Dicionário contendo:
                - conta_origem (str): número da conta de origem
                - cpf_destino (str): CPF do cliente destinatário
                - valor (float): valor a ser transferido
                - descricao (str): descrição opcional

            banco (opcional): parâmetro não utilizado (mantido por compatibilidade)

        Returns:
            dict: Resultado com 'sucesso' (bool) e 'mensagem' ou 'erros'
        """
        erros = []
        conta_origem_num = str(dados.get("conta_origem"))
        cpf_destino = dados.get("cpf_destino", "").strip()
        valor = dados.get("valor")

        if not conta_origem_num or not cpf_destino or valor is None:
            return {"sucesso": False, "erros": ["Dados obrigatórios ausentes."]}

        if not isinstance(valor, (int, float)) or valor <= 0:
            return {"sucesso": False, "erros": ["Valor inválido para transferência."]}

        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        cliente_destino = cliente_dao.buscar_por_id(cpf_destino)
        if not cliente_destino:
            return {"sucesso": False, "erros": [f"Destinatário com CPF {cpf_destino} não encontrado."]}

        conta_destino = next((c for c in cliente_destino.contas if c.get_estado_da_conta()), None)
        if not conta_destino:
            return {"sucesso": False, "erros": ["Destinatário não possui conta ativa."]}

        conta_origem = conta_dao.buscar_por_id(conta_origem_num)
        if not conta_origem:
            return {"sucesso": False, "erros": ["Conta de origem não encontrada."]}

        if conta_destino.get_numero_conta() == conta_origem.get_numero_conta():
            return {"sucesso": False, "erros": ["Não é possível transferir para a mesma conta."]}

        try:
            conta_origem.transferir(conta_destino, valor)
        except ContaInativaError as e:
            return {"sucesso": False, "erros": [str(e)]}
        except ValueError as e:
            return {"sucesso": False, "erros": [str(e)]}
        except Exception:
            return {"sucesso": False, "erros": ["Erro inesperado ao realizar a transferência."]}

        # Atualiza contas
        conta_dao.atualizar_objeto(conta_origem)
        conta_dao.atualizar_objeto(conta_destino)

        mensagem = f"Transferência de R$ {valor:.2f} realizada com sucesso para {cpf_destino}."
        return {"sucesso": True, "mensagem": mensagem}