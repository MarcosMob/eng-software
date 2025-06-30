# Ficheiro: tests/test_calculadora.py
# Descrição: Testes de unidade para a lógica de negócio (Model).

import pytest
from calculadora_pon import ParametrosPON, CalculadoraPON

# Cenário de teste 1: Um projeto viável
def test_calcular_margem_seguranca_viabilidade():
    """
    Testa o cálculo de uma margem de segurança positiva e viável.
    """
    params = ParametrosPON(
        p_tx_dbm=5.0,
        s_rx_dbm=-28.0,
        comprimento_km=15.0,
        atenuacao_db_km=0.25,
        perda_conector_db=0.5,
        num_conectores=4,
        perda_splitter_db=14.1, # Splitter 1:16
        margem_seguranca_db=None # Deixado em branco para ser calculado
    )
    calculadora = CalculadoraPON(params)
    resultado = calculadora.calcular()
    
    # O orçamento total é 33 dB. As perdas são 3.75 + 2 + 14.1 = 19.85 dB.
    # A margem deve ser 33 - 19.85 = 13.15 dB.
    assert "MARGEM DE SEGURANÇA: 13.15 dB" in resultado
    assert "O projeto é VIÁVEL" in resultado

# Cenário de teste 2: Um projeto inviável
def test_calcular_margem_negativa_inviavel():
    """
    Testa o cálculo de uma margem de segurança negativa, resultando em projeto inviável.
    """
    params = ParametrosPON(
        p_tx_dbm=2.0,
        s_rx_dbm=-25.0,
        comprimento_km=20.0,
        atenuacao_db_km=0.3,
        perda_conector_db=0.75,
        num_conectores=6,
        perda_splitter_db=17.5, # Splitter 1:32
        margem_seguranca_db=None
    )
    calculadora = CalculadoraPON(params)
    resultado = calculadora.calcular()

    # Orçamento: 27 dB. Perdas: 6 + 4.5 + 17.5 = 28 dB.
    # Margem: 27 - 28 = -1.00 dB.
    assert "MARGEM DE SEGURANÇA: -1.00 dB" in resultado
    assert "projeto é INVIÁVEL" in resultado

# Cenário de teste 3: Cálculo de outra variável (comprimento)
def test_calcular_comprimento_maximo():
    """
    Testa o cálculo do comprimento máximo da fibra.
    """
    params = ParametrosPON(
        p_tx_dbm=7.0,
        s_rx_dbm=-30.0,
        comprimento_km=None, # Deixado em branco para calcular
        atenuacao_db_km=0.22,
        perda_conector_db=0.3,
        num_conectores=2,
        perda_splitter_db=17.5, # Splitter 1:32
        margem_seguranca_db=3.0
    )
    calculadora = CalculadoraPON(params)
    resultado = calculadora.calcular()

    # Orçamento líquido: 37 - 3 = 34 dB.
    # Perdas fixas: 0.6 (conectores) + 17.5 (splitter) = 18.1 dB.
    # Orçamento para fibra: 34 - 18.1 = 15.9 dB.
    # Comprimento: 15.9 / 0.22 = 72.27 km.
    assert "Alcance Máximo da Fibra: 72.27 km" in resultado

# Cenário de teste 4: Teste de erro
def test_erro_multiplas_variaveis_vazias():
    """
    Verifica se uma exceção ValueError é levantada quando mais de um campo é deixado em branco.
    """
    params = ParametrosPON(
        p_tx_dbm=5.0,
        s_rx_dbm=-28.0,
        comprimento_km=None, # Vazio
        atenuacao_db_km=0.25,
        perda_conector_db=None, # Vazio
        num_conectores=4,
        perda_splitter_db=14.1,
        margem_seguranca_db=3.0
    )
    calculadora = CalculadoraPON(params)
    
    # Verifica se o código dentro do 'with' levanta a exceção esperada
    with pytest.raises(ValueError) as excinfo:
        calculadora.calcular()
    
    # Verifica se a mensagem de erro na exceção está correta
    assert "Mais de uma variável foi deixada em branco" in str(excinfo.value)

# ---