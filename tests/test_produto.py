import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.produto import Produto

class TestProduto(unittest.TestCase):
    
    def test_criar_produto(self):
        produto = Produto(1, "Arroz", 5.99, 100)
        self.assertEqual(produto.id_produto, 1)
        self.assertEqual(produto.nome, "Arroz")
        self.assertEqual(produto.preco, 5.99)
        self.assertEqual(produto.estoque, 100)
    
    def test_produto_sem_id(self):
        produto = Produto(None, "Feijão", 4.50, 50)
        self.assertIsNone(produto.id_produto)
        self.assertEqual(produto.nome, "Feijão")
        self.assertEqual(produto.preco, 4.50)
        self.assertEqual(produto.estoque, 50)
    
    def test_produto_preco_zero(self):
        produto = Produto(2, "Produto Grátis", 0.0, 10)
        self.assertEqual(produto.preco, 0.0)
    
    def test_produto_estoque_zero(self):
        produto = Produto(3, "Produto Esgotado", 10.00, 0)
        self.assertEqual(produto.estoque, 0)

if __name__ == '__main__':
    unittest.main()

