import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
from app.dao.cliente_dao import ClienteDAO
from app.models.cliente import Cliente

class TestClienteDAO(unittest.TestCase):
    
    def setUp(self):
        self.cliente_dao = ClienteDAO()
    
    @patch('app.dao.cliente_dao.get_db_connection')
    def test_create_cliente(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        cliente = Cliente(None, "João Silva", "joao@email.com", "senha123")
        resultado = self.cliente_dao.create(cliente)
        
        # Verificar se o método foi chamado corretamente
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        self.assertEqual(resultado.id_cliente, 1)
    
    @patch('app.dao.cliente_dao.get_db_connection')
    def test_get_all_clientes(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "João Silva", "joao@email.com", "senha123"),
            (2, "Maria Santos", "maria@email.com", "senha456")
        ]
        
        clientes = self.cliente_dao.get_all()
        
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0].nome, "João Silva")
        self.assertEqual(clientes[1].nome, "Maria Santos")
    
    @patch('app.dao.cliente_dao.get_db_connection')
    def test_get_by_id_cliente_existente(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "João Silva", "joao@email.com", "senha123")
        
        cliente = self.cliente_dao.get_by_id(1)
        
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nome, "João Silva")
    
    @patch('app.dao.cliente_dao.get_db_connection')
    def test_get_by_id_cliente_inexistente(self, mock_get_db):
        # Mock da conexão e cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        cliente = self.cliente_dao.get_by_id(999)
        
        self.assertIsNone(cliente)

if __name__ == '__main__':
    unittest.main()

