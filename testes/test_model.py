import unittest
from unittest.mock import patch, MagicMock 
from datetime import datetime


from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica
from model.cliente import Cliente
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca
from model.exceptions import ContaInativaError # não diretamente testado em Cliente, mas é uma dependência de Conta

# Constantes que podem ser usadas nos testes
from utils.constantes import TAXA_MANUTENCAO_CCORRENTE, RENDIMENTO_MENSAL_CPOUPANCA,LIMITE_TRANSFERENCIA_CCORRENTE,LIMITE_TRANSFERENCIA_CPOUPANCA




class TestPessoa(unittest.TestCase):
    def setUp(self):
        """
        ***************************************** Setup dos Testes *************************************************************
        O setUp prepara o ambiente para cada teste da classe e foi utilizado ao longo da maioria da classes de testes do grupo

        Aqui, ele cria instâncias de objetos necessários, como PessoaFisica e Cliente, e inicializa atributos comuns 
        para evitar repetição de código em cada teste.
        ********************************************************************************************************
        """
        # Inicia o patch da API de CEP (vale para todos os testes)
        self.patcher = patch(
            'utils.api.API.buscar_endereco_por_cep', 
            return_value="Rua Teste, 123 - Bairro Legal, Cidade Ficticia - UF, 12345-678"
        )
        self.mock_buscar_endereco = self.patcher.start()

        self.nome_pf = "Joao Silva"
        self.email_pf = "joao@email.com"
        self.cpf = "12345678900"
        self.cep = "12345678"
        self.num_endereco = "100"
        self.telefone_pf = "31999998888"
        self.data_nasc_str = "01/01/1990"
        self.data_nasc_dt = datetime(1990, 1, 1)
        self.endereco_mock = "Rua Mockada, 100 - Bairro Mock, Cidade Mock - MC, 12345678"

        self.pessoa_fisica = PessoaFisica(
            nome=self.nome_pf,
            email=self.email_pf,
            numero_documento=self.cpf,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco=self.endereco_mock,
            telefone=self.telefone_pf,
            data_nascimento=self.data_nasc_str
        )

        self.nome_pj = "Empresa XYZ"
        self.email_pj = "contato@xyz.com"
        self.cnpj = "12345678000199"
        self.telefone_pj = "3133334444"
        self.nome_fantasia = "XYZ Solucoes"

        self.pessoa_juridica = PessoaJuridica(
            nome=self.nome_pj,
            email=self.email_pj,
            numero_documento=self.cnpj,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco=self.endereco_mock,
            telefone=self.telefone_pj,
            nome_fantasia=self.nome_fantasia
        )

    def tearDown(self):
        # Para o patch da API de CEP após cada teste
        self.patcher.stop()

    def test_pessoa_fisica_criacao(self):
        """
        /************************ Teste 1 ****************************
        Verifica criação de PessoaFisica com todos os atributos básicos.

        Teste para garantir o armazenamento correto dos dados iniciais.
        ****************************************************************/
        """
        self.assertEqual(self.pessoa_fisica.get_nome(), self.nome_pf)
        self.assertEqual(self.pessoa_fisica.get_email(), self.email_pf)
        self.assertEqual(self.pessoa_fisica.get_numero_documento(), self.cpf)
        self.assertEqual(self.pessoa_fisica.get_data_nascimento(), self.data_nasc_dt)
        self.assertEqual(self.pessoa_fisica.get_tipo(), "fisica")
        self.assertEqual(self.pessoa_fisica.get_endereco(), "Rua Teste, 123 - Bairro Legal, Cidade Ficticia - UF, 12345-678")
        self.mock_buscar_endereco.assert_called_with(self.cep, self.num_endereco)

    def test_pessoa_fisica_str(self):
        """
        /************************ Teste 2 ****************************
        Verifica método __str__ de PessoaFisica.

        Importante para fins de exibição. 
        ****************************************************************/
        """
        self.assertEqual(str(self.pessoa_fisica), f"{self.nome_pf} (CPF: {self.cpf})")

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_fisica_instanciacao_com_data_nascimento_datetime(self, mock_api):
        """
        /************************ Teste 3 ****************************
        Verifica criação de PessoaFisica aceitando datetime para data de nascimento.

        Permite verificar se a classe aceita data_nascimento tanto em formato string quanto datetime.
        ****************************************************************/
        """
        pf = PessoaFisica(
            nome="Maria",
            email="m@m.com",
            numero_documento="98765432100",
            cep="87654321",
            numero_endereco="200",
            endereco="End Ficticio",
            telefone="31988887777",
            data_nascimento=datetime(1995, 5, 5)
        )
        self.assertEqual(pf.get_data_nascimento(), datetime(1995, 5, 5))

    def test_pessoa_juridica_criacao(self):
        """
        /************************ Teste 4 ****************************
        Verifica criação de PessoaJuridica com atributos básicos e nome fantasia.

        Teste para assegurar diferenciação entre pessoas físicas e jurídicas.
        ****************************************************************/
        """
        self.assertEqual(self.pessoa_juridica.get_nome(), self.nome_pj)
        self.assertEqual(self.pessoa_juridica.get_email(), self.email_pj)
        self.assertEqual(self.pessoa_juridica.get_numero_documento(), self.cnpj)
        self.assertEqual(self.pessoa_juridica.get_nome_fantasia(), self.nome_fantasia)
        self.assertEqual(self.pessoa_juridica.get_tipo(), "juridica")

    def test_pessoa_juridica_str(self):
        """
        /************************ Teste 5 ****************************
        Verifica método __str__ de PessoaJuridica.

        Teste para verificar a exibição clara de detalhes de empresas.
        ****************************************************************/
        """
        self.assertEqual(str(self.pessoa_juridica), f"{self.nome_fantasia} (CNPJ: {self.cnpj})")

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_juridica_sem_nome_fantasia(self, mock_api):
        """
        /************************ Teste 6 ****************************
        Verifica comportamento sem nome fantasia fornecido.

        Verifica se a ausência do nome fantasia é tratada corretamente como campo opcional
        ****************************************************************/
        """
        pj_sem_fantasia = PessoaJuridica(
            nome=self.nome_pj,
            email=self.email_pj,
            numero_documento=self.cnpj,
            cep=self.cep,
            numero_endereco=self.num_endereco,
            endereco="End Ficticio",
            telefone=self.telefone_pj
        )
        self.assertEqual(pj_sem_fantasia.get_nome_fantasia(), "")
        self.assertEqual(
            str(pj_sem_fantasia),
            f"Empresa sem nome fantasia (CNPJ: {self.cnpj})"
        )

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Endereco Mockado")
    def test_pessoa_fisica_cpf_invalido_gera_erro(self, mock_api):
        """
        /************************ Teste 7 ****************************
        Verifica que CPF inválido gera ValueError na criação de PessoaFisica.

        Esse teste é importante para validação de dados sensíveis e segurança.
        ****************************************************************/
        """
        with self.assertRaises(ValueError):
            PessoaFisica(
                nome="Nome Valido",
                email="email@valido.com",
                numero_documento="123",
                cep="12345678",
                numero_endereco="10",
                endereco="Rua X",
                telefone="31912345678",
                data_nascimento="01/01/2000"
            )

# --- Testes para Cliente
class TestCliente(unittest.TestCase):

    # Mock para a API de busca de endereço que é chamada no construtor de Pessoa
    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua Teste, 100 - Bairro Mock, Cidade Mock - MC, 12345-678")
    def setUp(self, mock_buscar_endereco_api):
        # Criando uma instância REAL de PessoaFisica
        self.dados_pessoa_fisica = {
            "nome": "Usuario Teste",
            "email": "usuario@teste.com",
            "numero_documento": "11122233344",
            "cep": "30100100",
            "numero_endereco": "100",
            "endereco": "Rua dos Testes, 100", 
            "telefone": "31912345678",
            "data_nascimento": "01/01/1990"
        }
        self.pessoa_real = PessoaFisica(**self.dados_pessoa_fisica)

        self.senha_correta = "Senha@Forte123"
        self.cliente = Cliente(pessoa=self.pessoa_real, senha=self.senha_correta)
        self.mock_buscar_endereco_api = mock_buscar_endereco_api 

    def test_cliente_criacao(self):
        """
        /************************ Teste 1 ****************************
         Testa a criação de um Cliente e a associação correta com uma Pessoa.
        *************************************************************/"""
        self.assertEqual(self.cliente.pessoa, self.pessoa_real)
        self.assertEqual(self.cliente.numero_documento, self.dados_pessoa_fisica["numero_documento"])
        self.assertTrue(self.cliente.verificar_senha(self.senha_correta))
    
        self.mock_buscar_endereco_api.assert_called_once_with(
            self.dados_pessoa_fisica["cep"], self.dados_pessoa_fisica["numero_endereco"]
        )


    def test_cliente_verificar_senha_incorreta(self):
        """
        /************************ Teste 2 ****************************
        Testa a verificação de senha com valor incorreto.
        
        Importante para a segurança do sistema, impedindo acessos indevidos.
        *************************************************************/"""
        self.assertFalse(self.cliente.verificar_senha("senhaErrada123"))

    def test_cliente_alterar_senha_sucesso(self):
        """
        /************************ Teste 3 ****************************
        Testa a alteração de senha com sucesso.

        Garante que o usuário consiga mudar sua senha de forma segura
        *************************************************************/
        """
        nova_senha = "NovaSenha@456"
        with patch('utils.validadores.validar_cliente.ValidarCliente.senha') as mock_validar_senha:
            self.cliente.alterar_senha(self.senha_correta, nova_senha)
            mock_validar_senha.assert_called_once_with(nova_senha) 
            self.assertTrue(self.cliente.verificar_senha(nova_senha))

    def test_cliente_alterar_senha_atual_incorreta(self):
        """
        /************************ Teste 4 ****************************
        Testa se o erro é levantado ao tentar alterar a senha com a senha atual errada.

        Permite testar se funciona o impedimento que uma senha seja trocada por alguém sem autenticação correta.
        *************************************************************/
        """
        with self.assertRaisesRegex(ValueError, "Senha atual incorreta."):
            self.cliente.alterar_senha("senhaAtualErrada", "NovaSenha@456")

    @patch('utils.validadores.validar_cliente.ValidarCliente.senha', side_effect=ValueError("Nova senha eh fraca"))
    def test_cliente_alterar_senha_nova_invalida(self, mock_validar_senha_com_erro):
        """
        /************************ Teste 5 ****************************
        Testa se erro é levantado ao tentar alterar a senha para uma senha nova inválida.
        *************************************************************/
        """
        with self.assertRaisesRegex(ValueError, "Nova senha eh fraca"):
            self.cliente.alterar_senha(self.senha_correta, "fraca123")
        mock_validar_senha_com_erro.assert_called_once_with("fraca123")


    def test_cliente_possui_conta(self):
        """
        /************************ Teste 6 ****************************
        Testa se o método possui_conta retorna True apenas quando o cliente realmente tem contas.

        Teste que permite ver o controle de cadastro e para a lógica da interface.
        *************************************************************/
        """
        self.assertFalse(self.cliente.possui_conta()) # 

        with patch('utils.validadores.validar_conta.ValidarConta.todos_campos', return_value=[]) as mock_validar_todos_campos_conta:
            conta_real_para_teste = ContaCorrente(numero="9999")
        self.cliente.contas = [conta_real_para_teste] 
        self.assertTrue(self.cliente.possui_conta())


    def test_cliente_criacao_tipo_pessoa_invalido(self):
        """
        /************************ Teste 7 ****************************
        Testa se TypeError é levantado quando o parâmetro 'pessoa' não é do tipo esperado.
        *************************************************************/
        """

        with self.assertRaisesRegex(TypeError, "O parâmetro 'pessoa' deve ser um objeto da classe Pessoa."):
            Cliente(pessoa="nao_eh_pessoa_obj", senha="123")

    def test_cliente_criacao_tipo_conta_invalido(self):
        """
        /************************ Teste 8 ****************************
        Testa se TypeError é levantado quando algum item em 'contas' não é do tipo Conta.

        Importante para garantir integridade dos dados.
         *************************************************************/
        """

        with patch('utils.validadores.validar_conta.ValidarConta.todos_campos', return_value=[]):
            conta_valida_real = ContaCorrente(numero="8888")

        with self.assertRaisesRegex(TypeError, "Todos os itens em 'contas' devem ser objetos da classe Conta."):
            Cliente(pessoa=self.pessoa_real, senha="123", contas=[conta_valida_real, "nao_eh_conta_obj"])



if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)






