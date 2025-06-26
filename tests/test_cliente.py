import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.cliente import Cliente

class TestCliente(unittest.TestCase):
    
    def test_criar_cliente(self):
        cliente = Cliente(1, "João Silva", "joao@email.com", "senha123")
        self.assertEqual(cliente.id_cliente, 1)
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.email, "joao@email.com")
        self.assertEqual(cliente.senha, "senha123")
    
    def test_cliente_sem_id(self):
        cliente = Cliente(None, "Maria Santos", "maria@email.com", "senha456")
        self.assertIsNone(cliente.id_cliente)
        self.assertEqual(cliente.nome, "Maria Santos")
        self.assertEqual(cliente.email, "maria@email.com")
        self.assertEqual(cliente.senha, "senha456")

if __name__ == '__main__':
    unittest.main()

