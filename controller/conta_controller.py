from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class ContaController:
    @staticmethod
    def obter_extrato(numero_conta: str):
        conta = ContaDAO().buscar_por_id(numero_conta)
        if not conta or not conta.get_estado_da_conta():
            return None, "Conta inválida ou inativa."
        return (conta.get_saldo(), conta.get_historico()), None

    @staticmethod
    def criar_conta(usuario_id: str, tipo_conta: str) -> dict:
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        cliente = cliente_dao.buscar_por_id(usuario_id)
        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}

        # Verifica se o cliente já tem uma conta do mesmo tipo
        for conta in cliente.contas:
            if (tipo_conta == TIPO_CCORRENTE and isinstance(conta, ContaCorrente)) or \
               (tipo_conta == TIPO_CPOUPANCA and isinstance(conta, ContaPoupanca)):
                return {"sucesso": False, "mensagem": f"Você já possui uma conta do tipo {tipo_conta}."}

        # Gera um novo número de conta único
        todas_contas = conta_dao.listar_todos_objetos()
        existentes = [int(c.get_numero_conta()) for c in todas_contas if c]
        novo_numero = str(max(existentes, default=1000) + 1)

        # Instancia a nova conta
        if tipo_conta == TIPO_CCORRENTE:
            nova_conta = ContaCorrente(numero=novo_numero)
        elif tipo_conta == TIPO_CPOUPANCA:
            nova_conta = ContaPoupanca(numero=novo_numero)
        else:
            return {"sucesso": False, "mensagem": "Tipo de conta inválido."}

        # Salva a nova conta
        conta_dao.salvar_objeto(nova_conta)

        cliente.contas.append(nova_conta)
        cliente_dao.atualizar_objeto(cliente)
        return {"sucesso": True, "mensagem": f"Conta {novo_numero} criada com sucesso!"}

    @staticmethod
    def listar_contas(usuario_id: str):
        cliente = ClienteDAO().buscar_por_id(usuario_id)
        if not cliente:
            return []
        return cliente.contas

    @staticmethod
    def excluir_conta(usuario_id: str, numero_conta: str, senha: str) -> dict:
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        cliente = cliente_dao.buscar_por_id(usuario_id)
        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}

        if not cliente.verificar_senha(senha):
            return {"sucesso": False, "mensagem": "Senha incorreta."}

        conta = next((c for c in cliente.contas if c.get_numero_conta() == numero_conta), None)
        if not conta or not conta.get_estado_da_conta():
            return {"sucesso": False, "mensagem": "Conta não encontrada ou já inativa."}

        conta.encerrar_conta()
        conta_dao.atualizar_objeto(conta)
        cliente_dao.atualizar_objeto(cliente)

        return {"sucesso": True, "mensagem": f"Conta {numero_conta} encerrada com sucesso."}