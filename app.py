from flask import Flask, render_template, request, flash

# Importa as classes e constantes do nosso módulo de lógica
from calculadora_pon import ParametrosPON, CalculadoraPON, FAIXAS_TIPICAS, SPLITTER_PERDAS

app = Flask(__name__)
# Chave secreta necessária para usar 'flash messages', mas não a usaremos aqui.
# É uma boa prática incluí-la.
app.secret_key = 'super-secret-key' 

def converter_para_numerico(valor_str, tipo_dado=float):
    """
    Converte uma string do formulário para float/int ou None se estiver vazia.
    A vírgula é substituída por ponto para aceitar ambos os formatos.
    """
    if valor_str is None or valor_str.strip() == '':
        return None
    try:
        return tipo_dado(valor_str.replace(',', '.'))
    except (ValueError, TypeError):
        return None # Retorna None se a conversão falhar

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    # Passamos os dicionários para o template para que ele possa exibir as faixas típicas
    # e as opções de splitter dinamicamente.
    return render_template('index.html', faixas=FAIXAS_TIPICAS, splitters=SPLITTER_PERDAS)

@app.route('/calcular', methods=['POST'])
def calcular():
    """Recebe os dados do formulário, executa o cálculo e exibe o resultado."""
    try:
        # 1. Coletar e converter dados do formulário
        params_data = {
            'p_tx_dbm': converter_para_numerico(request.form.get('p_tx_dbm')),
            's_rx_dbm': converter_para_numerico(request.form.get('s_rx_dbm')),
            'comprimento_km': converter_para_numerico(request.form.get('comprimento_km')),
            'atenuacao_db_km': converter_para_numerico(request.form.get('atenuacao_db_km')),
            'perda_conector_db': converter_para_numerico(request.form.get('perda_conector_db')),
            'num_conectores': converter_para_numerico(request.form.get('num_conectores'), int),
            'perda_splitter_db': converter_para_numerico(request.form.get('perda_splitter_db')),
            'margem_seguranca_db': converter_para_numerico(request.form.get('margem_seguranca_db')),
        }

        # 2. Instanciar o modelo de dados e a calculadora
        parametros = ParametrosPON(**params_data)
        calculadora = CalculadoraPON(parametros)

        # 3. Executar validação e cálculo
        alertas = parametros.validar_valores()
        resultado = calculadora.calcular()

        # 4. Renderizar a página de resultado com os dados obtidos
        return render_template('resultado.html', resultado=resultado, alertas=alertas)

    except ValueError as e:
        # Captura erros específicos da nossa lógica (ex: mais de uma variável vazia)
        resultado_erro = f"ERRO NA VALIDAÇÃO: {e}"
        return render_template('resultado.html', resultado=resultado_erro, alertas=[])
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        resultado_erro = f"Ocorreu um erro inesperado no servidor: {e}"
        return render_template('resultado.html', resultado=resultado_erro, alertas=[])

if __name__ == '__main__':
    # Executa a aplicação em modo de depuração (ótimo para desenvolvimento)
    app.run(debug=True)