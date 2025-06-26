from flask import Flask, render_template
from app.controllers.cliente_controller import cliente_bp
from app.controllers.produto_controller import produto_bp

app = Flask(__name__)
app.secret_key = 'supermercado_secret_key'

# Registrar blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(produto_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

