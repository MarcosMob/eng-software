from app.database import get_db_connection
from app.models.produto import Produto

class ProdutoDAO:
    def create(self, produto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s) RETURNING id_produto",
            (produto.nome, produto.preco, produto.estoque)
        )
        produto.id_produto = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return produto

    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nome, preco, estoque FROM produtos")
        produtos = []
        for row in cursor.fetchall():
            produtos.append(Produto(row[0], row[1], row[2], row[3]))
        cursor.close()
        conn.close()
        return produtos

    def get_by_id(self, id_produto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_produto, nome, preco, estoque FROM produtos WHERE id_produto = %s", (id_produto,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Produto(row[0], row[1], row[2], row[3])
        return None

    def update(self, produto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = %s, preco = %s, estoque = %s WHERE id_produto = %s",
            (produto.nome, produto.preco, produto.estoque, produto.id_produto)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, id_produto):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
        conn.commit()
        cursor.close()
        conn.close()


