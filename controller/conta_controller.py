from dao.cliente_dao import ClienteDAO
from dao.conta_dao import ContaDAO
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from utils.constantes import TIPO_CCORRENTE, TIPO_CPOUPANCA


class ContaController:
    """
    Controlador responsável pelas operações sobre contas bancárias:
    criação, listagem, exclusão e consulta de extrato.
    """

    @staticmethod
    def obter_extrato(numero_conta: str):
        """
        Retorna o saldo e o histórico de transações de uma conta ativa.

        Args:
            numero_conta (str): Número da conta a ser consultada.

        Returns:
            Tuple[(float, list), None] em caso de sucesso,
            ou (None, str) com mensagem de erro.
        """
        conta = ContaDAO().buscar_por_id(numero_conta)

        if not conta or not conta.get_estado_da_conta():
            return None, "Conta inválida ou inativa."

        return (conta.get_saldo(), conta.get_historico()), None

    @staticmethod
    def criar_conta(usuario_id: str, tipo_conta: str) -> dict:
        """
        Cria uma nova conta para um cliente, garantindo que ele não possua conta do mesmo tipo.

        Args:
            usuario_id (str): CPF ou CNPJ do cliente.
            tipo_conta (str): Tipo da conta (corrente ou poupança).

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
        cliente_dao = ClienteDAO()
        conta_dao = ContaDAO()

        cliente = cliente_dao.buscar_por_id(usuario_id)
        if not cliente:
            return {"sucesso": False, "mensagem": "Cliente não encontrado."}

        # Verifica se o cliente já possui uma conta do tipo informado
        for conta in cliente.contas:
            if (tipo_conta == TIPO_CCORRENTE and isinstance(conta, ContaCorrente)) or \
               (tipo_conta == TIPO_CPOUPANCA and isinstance(conta, ContaPoupanca)):
                return {"sucesso": False, "mensagem": f"Você já possui uma conta do tipo {tipo_conta}."}

        # Geração de número único de conta
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

        # Persiste a nova conta e atualiza cliente
        conta_dao.salvar_objeto(nova_conta)
        cliente.contas.append(nova_conta)
        cliente_dao.atualizar_objeto(cliente)

        return {"sucesso": True, "mensagem": f"Conta {novo_numero} criada com sucesso!"}

    @staticmethod
    def listar_contas(usuario_id: str):
        """
        Lista todas as contas associadas a um cliente.

        Args:
            usuario_id (str): CPF ou CNPJ do cliente.

        Returns:
            list: Lista de contas do cliente (pode estar vazia).
        """
        cliente = ClienteDAO().buscar_por_id(usuario_id)
        return cliente.contas if cliente else []

    @staticmethod
    def excluir_conta(usuario_id: str, numero_conta: str, senha: str) -> dict:
        """
        Encerra uma conta do cliente, após validação da senha.

        Args:
            usuario_id (str): Documento do cliente.
            numero_conta (str): Número da conta a ser encerrada.
            senha (str): Senha do cliente.

        Returns:
            dict: Resultado da operação com status e mensagem.
        """
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
    
    @staticmethod
    def contas_ativas_para_dropdown(cliente):
        """
        Retorna uma lista de opções para dropdown com as contas ativas do cliente.

        Args:
            cliente: Objeto Cliente.

        Returns:
            list[str]: Lista de strings com os números das contas ativas.
        """
        return [
            str(conta.get_numero_conta())
            for conta in cliente.contas if conta.get_estado_da_conta()
        ]
