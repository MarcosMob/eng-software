Calculadora PON WebUma aplicação web construída com Flask para calcular o orçamento de potência e outros parâmetros essenciais em projetos de Redes Ópticas Passivas (PON).
Sobre o ProjetoEste projeto transforma uma ferramenta de linha de comando (CLI) em Python numa interface web interativa e amigável. O objetivo é fornecer a estudantes, técnicos e engenheiros de redes uma calculadora flexível para projetar e validar enlaces ópticos em redes PON (GPON, EPON, etc.).A aplicação permite que o utilizador preencha os parâmetros conhecidos de um enlace óptico e deixe em branco o valor que deseja descobrir. A lógica de negócio, encapsulada em classes Python, realiza o cálculo e retorna o resultado de forma clara, incluindo alertas e recomendações. Funcionalidades PrincipaisCálculo Flexível: Deixe qualquer um dos campos em branco para que a aplicação calcule o valor correspondente.Análise de Viabilidade: Calcula a margem de segurança do projeto, indicando se o enlace é viável, arriscado ou inviável.Cálculo de Parâmetros:Margem de Segurança ResultanteAlcance Máximo da Fibra (em km)Potência de Transmissão (Tx) Mínima NecessáriaSensibilidade de Recepção (Rx) Máxima SuportadaPerda Máxima para o Splitter (com recomendação de modelo)Atenuação Máxima da Fibra (dB/km)Número Máximo de ConectoresPerda Máxima por ConectorValidação de Entradas: Emite alertas caso os valores inseridos estejam fora das faixas típicas de mercado, ajudando a evitar erros de projeto.Interface Web Intuitiva: Um formulário simples e direto, fácil de usar em qualquer navegador. Tecnologias UtilizadasBackend:Python 3FlaskFrontend:HTML5CSS3Arquitetura:Separação clara entre a lógica de negócio (calculadora_pon.py), o controlador (app.py) e a visão (templates/). Como Executar o ProjetoSiga os passos abaixo para executar a aplicação na sua máquina local.
1. Clone o Repositóriogit clone https://github.com/MarcosMob/eng-software/tree/propag
cd calculadora-pon-web

2. Crie e Ative um Ambiente VirtualÉ uma boa prática isolar as dependências do projeto.Windows:python -m venv venv
.\venv\Scripts\activate
macOS / Linux:python3 -m venv venv
source venv/bin/activate
3. Instale as DependênciasO ficheiro requirements.txt contém a única dependência necessária: Flask.pip install -r requirements.txt
4. Execute a Aplicação Flaskflask run
A aplicação será executada em modo de depuração.5. Aceda no NavegadorAbra o seu navegador e vá para o seguinte endereço:http://127.0.0.1:5000
Estrutura de FicheirosO projeto está organizado da seguinte forma para manter uma clara separação de responsabilidades:/calculadora-pon-web/
├── app.py                  # Controlador Flask: gere as rotas e a lógica da web.
├── calculadora_pon.py        # Modelo e Lógica de Negócio: contém as classes de cálculo.
├── requirements.txt        # Lista de dependências Python do projeto.
│
├── static/                   # Ficheiros estáticos (CSS, JS, Imagens).
│   └── css/
│       └── style.css         # Folha de estilos para a interface.
│
└── templates/                # Templates HTML (a "Visão" da aplicação).
    ├── index.html            # Página principal com o formulário de entrada.
    └── resultado.html        # Página que exibe os resultados do cálculo.