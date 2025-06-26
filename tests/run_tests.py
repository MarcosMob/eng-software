import unittest
import sys
import os

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar todos os módulos de teste
from test_cliente import TestCliente
from test_produto import TestProduto
from test_cliente_dao import TestClienteDAO
from test_produto_dao import TestProdutoDAO

def run_all_tests():
    # Criar uma suite de testes
    test_suite = unittest.TestSuite()
    
    # Adicionar testes dos modelos
    test_suite.addTest(unittest.makeSuite(TestCliente))
    test_suite.addTest(unittest.makeSuite(TestProduto))
    
    # Adicionar testes dos DAOs
    test_suite.addTest(unittest.makeSuite(TestClienteDAO))
    test_suite.addTest(unittest.makeSuite(TestProdutoDAO))
    
    # Executar os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    print("Executando todos os testes do sistema...")
    print("=" * 50)
    result = run_all_tests()
    
    if result.wasSuccessful():
        print("\n" + "=" * 50)
        print("TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print("\n" + "=" * 50)
        print(f"FALHAS: {len(result.failures)}")
        print(f"ERROS: {len(result.errors)}")

