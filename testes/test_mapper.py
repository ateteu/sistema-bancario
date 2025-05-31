import unittest
from unittest.mock import patch
from datetime import datetime

from mapper.pessoa_mapper import PessoaMapper
from model.pessoa_fisica import PessoaFisica
from model.pessoa_juridica import PessoaJuridica

from mapper.conta_mapper import ContaMapper
from model.conta_corrente import ContaCorrente
from model.conta_poupanca import ContaPoupanca

from utils.constantes import (
    TIPO_PFISICA,
    TIPO_PJURIDICA,
    TIPO_CCORRENTE,
    TIPO_CPOUPANCA
)


class TestPessoaMapper(unittest.TestCase):

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua Mockada, 123 - Bairro, Cidade - UF, 00000-000")
    def test_from_dict_pessoa_fisica_sucesso(self, mock_api_cep):
        """
        /************************ Teste 1 ****************************
        Testa a conversão de um dicionário para uma instância de PessoaFisica.

        Teste para garantir que dados vindos de fontes externas sejam mapeados corretamente,
        incluindo chamada da API de CEP que foi previamente escolhida pelo grupo.
        *****************************************************************/
        """
        dados_pf = {
            "tipo": TIPO_PFISICA,
            "nome": "Victor",
            "email": "victor@email.com",
            "numero_documento": "12345678900",
            "cep": "12345000",
            "numero_endereco": "10",
            "endereco": "Rua dos Testes, 0",
            "telefone": "31999998888",
            "data_nascimento": "01/01/1990"
        }

        pessoa = PessoaMapper.from_dict(dados_pf)

        self.assertIsInstance(pessoa, PessoaFisica)
        self.assertEqual(pessoa.get_nome(), dados_pf["nome"])
        self.assertEqual(pessoa.get_email(), dados_pf["email"])
        self.assertEqual(pessoa.get_numero_documento(), dados_pf["numero_documento"])
        self.assertEqual(pessoa.get_data_nascimento(), datetime(1990, 1, 1))
        mock_api_cep.assert_called_once_with(dados_pf["cep"], dados_pf["numero_endereco"])

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Av. Mock, 456 - Centro, Metropole - MT, 11111-000")
    def test_from_dict_pessoa_juridica_sucesso(self, mock_api_cep):
        """
        /************************ Teste 2 ****************************
        Testa a conversão de um dicionário para PessoaJuridica com nome fantasia.

        Teste para verificar a instância correta e uso opcional de nome fantasia.
        *****************************************************************/
        """
        dados_pj = {
            "tipo": TIPO_PJURIDICA,
            "nome": "Empresa Victor SA",
            "email": "contato@email.com",
            "numero_documento": "12345678000199",
            "cep": "70000100",
            "numero_endereco": "S/N",
            "endereco": "Praça Principal, S/N",
            "telefone": "6132109876",
            "nome_fantasia": "Modelo Fantasia"
        }

        pessoa = PessoaMapper.from_dict(dados_pj)

        self.assertIsInstance(pessoa, PessoaJuridica)
        self.assertEqual(pessoa.get_nome(), dados_pj["nome"])
        self.assertEqual(pessoa.get_numero_documento(), dados_pj["numero_documento"])
        self.assertEqual(pessoa.get_nome_fantasia(), dados_pj["nome_fantasia"])
        mock_api_cep.assert_called_once_with(dados_pj["cep"], dados_pj["numero_endereco"])

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua Mockada, 123 - Bairro, Cidade - UF, 00000-000")
    def test_from_dict_pessoa_juridica_sem_nome_fantasia(self, mock_api_cep):
        """
        /************************ Teste 3 ****************************
        Testa a conversão de dict para PessoaJuridica sem nome fantasia.

        Teste para confirmar que o atributo opcional é tratado como vazio.
        *****************************************************************/
        """
        dados_pj = {
            "tipo": TIPO_PJURIDICA,
            "nome": "Outra Empresa Ltda",
            "email": "financeiro@email.co",
            "numero_documento": "98765432000100",
            "cep": "54321000",
            "numero_endereco": "1000",
            "endereco": "Rua Secundaria, 1000",
            "telefone": "2122334455"
        }

        pessoa = PessoaMapper.from_dict(dados_pj)

        self.assertIsInstance(pessoa, PessoaJuridica)
        self.assertEqual(pessoa.get_nome_fantasia(), "")

    def test_from_dict_tipo_desconhecido(self):
        """
        /************************ Teste 4 ****************************
        Testa ValueError ao receber tipo de pessoa desconhecido no dict.

        Testes relacionados com mapeamentos inválidos e indicação de erro claro.
        *****************************************************************/
        """
        dados_errados = {"tipo": "argentino", "nome": "arg"}
        with self.assertRaisesRegex(ValueError, "Tipo de pessoa desconhecido: arg"):
            PessoaMapper.from_dict(dados_errados)

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua dos Testes, 0")
    def test_from_dict_campo_obrigatorio_faltando_para_modelo(self, mock_api):
        """
        /************************ Teste 5 ****************************
        Testa KeyError quando campo obrigatório está ausente no dict.

        Teste para verificar se construtores de modelo estão falhando adequadamente.
        *****************************************************************/
        """
        dados_pf_sem_nome = {
            "tipo": TIPO_PFISICA,
            "email": "victor@email.com",
            "numero_documento": "12345678900",
            "cep": "12345000",
            "numero_endereco": "10",
            "endereco": "Rua dos Testes, 0",
            "telefone": "31999998888",
            "data_nascimento": "01/01/1990"
        }

        with self.assertRaises(KeyError):
            PessoaMapper.from_dict(dados_pf_sem_nome)

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Rua Mockada")
    def test_to_dict_pessoa_fisica(self, mock_api_cep):
        """
        /************************ Teste 6 ****************************
        Testa a conversão de PessoaFisica para dict.

        Para verificar o formato correto de saída, incluindo data formatada.
        *****************************************************************/
        """
        pessoa_pf = PessoaFisica(
            nome="Victor Silva",
            email="victor_silv@teste.net",
            numero_documento="00987654321",
            cep="87654321",
            numero_endereco="SN",
            endereco="Viela Teste, SN",
            telefone="41977776666",
            data_nascimento=datetime(1985, 5, 15)
        )

        dict_pessoa = PessoaMapper.to_dict(pessoa_pf)

        self.assertEqual(dict_pessoa["tipo"], TIPO_PFISICA)
        self.assertEqual(dict_pessoa["nome"], "Victor Silva")
        self.assertEqual(dict_pessoa["numero_documento"], "00987654321")
        self.assertEqual(dict_pessoa["data_nascimento"], "15/05/1985")
        self.assertNotIn("nome_fantasia", dict_pessoa)

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Av. Teste")
    def test_to_dict_pessoa_juridica_com_fantasia(self, mock_api_cep):
        """
        /************************ Teste 7 ****************************
        Testa a conversão de PessoaJuridica com nome fantasia para dict.

        Teste para validar  a correta inclusão de nome fantasia e omissão de campos irrelevantes.
        *****************************************************************/
        """
        pessoa_pj = PessoaJuridica(
            nome="Comércio Teste e Filhos",
            email="vendas@comercio.co",
            numero_documento="00112233000144",
            cep="12121200",
            numero_endereco="123",
            endereco="Rua Comercial, 123",
            telefone="1120304050",
            nome_fantasia="Teste Fantasia Comércio"
        )

        dict_pessoa = PessoaMapper.to_dict(pessoa_pj)

        self.assertEqual(dict_pessoa["tipo"], TIPO_PJURIDICA)
        self.assertEqual(dict_pessoa["nome"], "Comércio Teste e Filhos")
        self.assertEqual(dict_pessoa["nome_fantasia"], "Teste Fantasia Comércio")
        self.assertNotIn("data_nascimento", dict_pessoa)

    @patch('utils.api.API.buscar_endereco_por_cep', return_value="Av. Teste")
    def test_to_dict_pessoa_juridica_sem_fantasia_preenchido(self, mock_api_cep):
        """
        /************************ Teste 8 ****************************
        Testa a conversão de PessoaJuridica sem nome fantasia válido.

        Teste para confirmar que nome fantasia vazio ealmente não aparece no dict.
        *****************************************************************/
        """
        pessoa_pj = PessoaJuridica(
            nome="Outra Empresa SA",
            email="contato@outraempresa.com",
            numero_documento="33445566000177",
            cep="30303000",
            numero_endereco="Apto 1",
            endereco="Rua Empresarial, Apto 1",
            telefone="2150607080",
            nome_fantasia="   "
        )

        dict_pessoa = PessoaMapper.to_dict(pessoa_pj)

        self.assertEqual(dict_pessoa["tipo"], TIPO_PJURIDICA)
        self.assertNotIn("nome_fantasia", dict_pessoa)

