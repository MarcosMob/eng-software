from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.dao.produto_dao import ProdutoDAO
from app.models.produto import Produto

produto_bp = Blueprint('produto', __name__)
produto_dao = ProdutoDAO()

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = produto_dao.get_all()
    return render_template('produtos/listar.html', produtos=produtos)

@produto_bp.route('/produtos/novo', methods=['GET'])
def novo_produto():
    return render_template('produtos/novo.html')

@produto_bp.route('/produtos', methods=['POST'])
def criar_produto():
    nome = request.form['nome']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])
    
    produto = Produto(None, nome, preco, estoque)
    produto_dao.create(produto)
    
    return redirect(url_for('produto.listar_produtos'))

@produto_bp.route('/produtos/<int:id_produto>/editar', methods=['GET'])
def editar_produto(id_produto):
    produto = produto_dao.get_by_id(id_produto)
    return render_template('produtos/editar.html', produto=produto)

@produto_bp.route('/produtos/<int:id_produto>', methods=['POST'])
def atualizar_produto(id_produto):
    nome = request.form['nome']
    preco = float(request.form['preco'])
    estoque = int(request.form['estoque'])
    
    produto = Produto(id_produto, nome, preco, estoque)
    produto_dao.update(produto)
    
    return redirect(url_for('produto.listar_produtos'))

@produto_bp.route('/produtos/<int:id_produto>/excluir', methods=['POST'])
def excluir_produto(id_produto):
    produto_dao.delete(id_produto)
    return redirect(url_for('produto.listar_produtos'))

