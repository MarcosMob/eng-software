import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
from app.dao.produto_dao import ProdutoDAO
from app.models.produto import Produto

class TestProdutoDAO(unittest.TestCase):
    
    def setUp(self):
        self.produto_dao = ProdutoDAO()
    
    @patch('app.dao.produto_dao.get_db_connection')
    def test_create_produto(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        produto = Produto(None, "Arroz", 5.99, 100)
        resultado = self.produto_dao.create(produto)
        
        # Verificar se o método foi chamado corretamente
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        self.assertEqual(resultado.id_produto, 1)
    
    @patch('app.dao.produto_dao.get_db_connection')
    def test_get_all_produtos(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Arroz", 5.99, 100),
            (2, "Feijão", 4.50, 50)
        ]
        
        produtos = self.produto_dao.get_all()
        
        self.assertEqual(len(produtos), 2)
        self.assertEqual(produtos[0].nome, "Arroz")
        self.assertEqual(produtos[1].nome, "Feijão")
    
    @patch('app.dao.produto_dao.get_db_connection')
    def test_update_produto(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        produto = Produto(1, "Arroz Integral", 6.99, 80)
        self.produto_dao.update(produto)
        
        # Verificar se o método foi chamado corretamente
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('app.dao.produto_dao.get_db_connection')
    def test_delete_produto(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        self.produto_dao.delete(1)
        
        # Verificar se o método foi chamado corretamente
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()

