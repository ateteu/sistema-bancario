from utils.logger import logger
from dao.pessoa_dao import PessoaDAO
from dao.cliente_dao import ClienteDAO
from model.pessoa_fisica import PessoaFisica
from utils.validadores.validar_pessoa import ValidarPessoa as Validar

class PerfilController:
    """
    Controlador responsável por gerenciar a visualização e edição
    do perfil do cliente, incluindo atualização de dados pessoais
    e alteração de senha.
    """

    @staticmethod
    def obter_dados_perfil(documento: str) -> dict:
        """
        Obtém os dados do perfil do cliente (dados pessoais e informações básicas).

        Args:
            documento (str): CPF/CNPJ do cliente.

        Returns:
            dict: Dados do cliente e pessoa ou mensagem de erro.
        """
        logger.info(f"Buscando dados de perfil para documento: {documento}")
        try:
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {
                    "status"   : "erro", 
                    "mensagem" : "Cliente não encontrado."
                }

            pessoa = cliente.pessoa
            dados = {
                "nome"             : pessoa.get_nome(),
                "email"            : pessoa.get_email(),
                "numero_documento" : pessoa.get_numero_documento(),
                "cep"              : pessoa.get_cep(),
                "numero_endereco"  : pessoa.get_numero_endereco(),
                "telefone"         : pessoa.get_telefone()
            }
            if isinstance(pessoa, PessoaFisica):
                data_nascimento = pessoa.get_data_nascimento()

                # Converte a data de datetime para str (ex: 20/04/2025)
                dados["data_nascimento"] = data_nascimento.strftime("%d/%m/%Y")
            else:
                return {
                    "status"   : "erro", 
                    "mensagem" : "O usuário cadastrado é uma Pessoa de um tipo não reconhecido."
                }

            return {
                "status" : "sucesso", 
                "dados"  : dados
            }
        except Exception as e:
            logger.error(f"Erro ao obter dados do perfil: {e}")
            return {
                "status"   : "erro", 
                "mensagem" : "Erro ao obter dados do perfil."
            }

    @staticmethod
    def atualizar_dados_perfil(documento: str, dados_atualizados: dict) -> dict:
        """
        Atualiza dados mutáveis do perfil do cliente.

        Args:
            documento (str): CPF/CNPJ do cliente.
            dados_atualizados (dict): Dados para atualização.

        Returns:
            dict: Resultado da operação (contendo status e mensagem).
        """
        logger.info(f"Iniciando atualização de dados do perfil para documento: {documento}")
        
        try:
            # Busca para ver se o cliente (pessoa com cpf/cnpj tal) existe
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {
                    "status"   : "erro", 
                    "mensagem" : "Cliente não encontrado."
                }

            pessoa = cliente.pessoa
            
            # Preenche variáveis com os dados enviados ou os atuais
            nome            = dados_atualizados.get("nome", pessoa.get_nome())
            email           = dados_atualizados.get("email", pessoa.get_email())
            cep             = dados_atualizados.get("cep", pessoa.get_cep())
            numero_endereco = dados_atualizados.get("numero_endereco", pessoa.get_numero_endereco())
            telefone        = dados_atualizados.get("telefone", pessoa.get_telefone())

            # Valida tudo em conjunto
            erros = Validar._campos_comuns(nome, email, cep, numero_endereco, telefone)
            if erros:
                # Retorna todos os erros de validação dos campos
                return {
                    "status"   : "erro", 
                    "mensagem" : "Erro(s) de validação:\n" + "\n".join(erros)
                }

            # Aplica os setters com os dados já validados
            if "nome" in dados_atualizados:
                pessoa.set_nome(nome)
            if "email" in dados_atualizados:
                pessoa.set_email(email)
            if "cep" in dados_atualizados:
                pessoa.set_cep(cep)
            if "numero_endereco" in dados_atualizados:
                pessoa.set_numero_endereco(numero_endereco)
            if "telefone" in dados_atualizados:
                pessoa.set_telefone(telefone)

            # Atualiza Pessoa e Cliente no banco de dados
            PessoaDAO().atualizar_objeto(pessoa)
            ClienteDAO().atualizar_objeto(cliente)

            return {
                "status"   : "sucesso", 
                "mensagem" : "Dados do perfil atualizados com sucesso."
            }
        except Exception as e:
            logger.error(f"Erro ao atualizar dados do perfil: {e}")
            return {
                "status"   : "erro", 
                "mensagem" : "Erro ao atualizar dados do perfil."
            }

    @staticmethod
    def alterar_senha(documento: str, senha_atual: str, nova_senha: str) -> dict:
        """
        Altera a senha do cliente, validando a senha atual e a qualidade da nova senha.

        Args:
            documento (str): CPF/CNPJ do cliente.
            senha_atual (str): Senha atual do cliente.
            nova_senha (str): Nova senha desejada.

        Returns:
            dict: Resultado da operação.
        """
        logger.info(f"Solicitação de alteração de senha para documento: {documento}")
        
        try:
            # Busca para ver se o cliente (pessoa com cpf/cnpj tal) existe
            cliente = ClienteDAO().buscar_por_id(documento)
            if cliente is None:
                return {
                    "status"   : "erro",
                    "mensagem" : "Cliente não encontrado."
                }

            # Tenta atualizar a senha
            try:
                cliente.alterar_senha(senha_atual, nova_senha)
            except ValueError as e:
                return {
                    "status"   : "erro",
                    "mensagem" : str(e)
                }

            # Atualiza o objeto no banco de dados
            ClienteDAO().atualizar_objeto(cliente)

            return {
                "status"   : "sucesso",
                "mensagem" : "Senha alterada com sucesso."
            }
        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return {
                "status"   : "erro",
                "mensagem" : "Erro inesperado ao tentar alterar senha."
            }
