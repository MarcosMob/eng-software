# Ficheiro: tests/test_app.py
# Descrição: Testes de integração para as rotas Flask (Controller).

import pytest
from app import app as flask_app # Renomeia para evitar conflito de nome

@pytest.fixture
def client():
    """Cria um cliente de teste para a aplicação Flask."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_pagina_inicial(client):
    """
    Testa se a página inicial (rota '/') carrega corretamente.
    """
    response = client.get('/')
    assert response.status_code == 200
    # Verifica se o título está presente no HTML
    assert b"Calculadora Flex" in response.data

def test_calculo_sucesso_integracao(client):
    """
    Testa o fluxo completo de um cálculo bem-sucedido através de uma requisição POST.
    """
    # Dados do formulário que seriam enviados por um navegador
    form_data = {
        'p_tx_dbm': '5.0',
        's_rx_dbm': '-28.0',
        'comprimento_km': '15.0',
        'atenuacao_db_km': '0.25',
        'perda_conector_db': '0.5',
        'num_conectores': '4',
        'perda_splitter_db': '14.1',
        'margem_seguranca_db': '' # Campo a ser calculado
    }
    response = client.post('/calcular', data=form_data)
    assert response.status_code == 200
    # Verifica se o resultado está na página de resposta
    assert b"MARGEM DE SEGURANCA: 13.15 dB" in response.data
    assert b"O projeto &eacute; VI&Aacute;VEL" in response.data # HTML codifica caracteres especiais

def test_calculo_erro_integracao(client):
    """
    Testa o fluxo de um cálculo com erro (múltiplos campos vazios).
    """
    form_data = {
        'p_tx_dbm': '5.0',
        's_rx_dbm': '-28.0',
        'comprimento_km': '', # Vazio
        'atenuacao_db_km': '0.25',
        'perda_conector_db': '', # Vazio
        'num_conectores': '4',
        'perda_splitter_db': '14.1',
        'margem_seguranca_db': '3.0'
    }
    response = client.post('/calcular', data=form_data)
    assert response.status_code == 200 # A página de erro ainda deve carregar com sucesso
    assert b"ERRO NA VALIDA" in response.data
    assert b"Mais de uma vari" in response.data