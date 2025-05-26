from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.exceptions import ContaInativaError

class PagamentoController:
    @staticmethod
    def processar_pagamento(conta_origem_num: int, cpf_destino: str, valor: float, descricao: str) -> dict:
        erros = []

        if not cpf_destino or valor is None or conta_origem_num is None:
            return {"sucesso": False, "erros": ["Preencha todos os campos obrigatórios."]}

        if valor <= 0:
            return {"sucesso": False, "erros": ["O valor deve ser maior que zero."]}

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

        conta_dao.atualizar_objeto(conta_origem)
        conta_dao.atualizar_objeto(conta_destino)

        return {"sucesso": True, "mensagem": f"Transferência de R$ {valor:.2f} realizada com sucesso."}
