from app.database import get_db_connection
from app.models.cliente import Cliente

class ClienteDAO:
    def create(self, cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_cliente",
            (cliente.nome, cliente.email, cliente.senha)
        )
        cliente.id_cliente = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return cliente

    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome, email, senha FROM clientes")
        clientes = []
        for row in cursor.fetchall():
            clientes.append(Cliente(row[0], row[1], row[2], row[3]))
        cursor.close()
        conn.close()
        return clientes

    def get_by_id(self, id_cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nome, email, senha FROM clientes WHERE id_cliente = %s", (id_cliente,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Cliente(row[0], row[1], row[2], row[3])
        return None

    def update(self, cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET nome = %s, email = %s, senha = %s WHERE id_cliente = %s",
            (cliente.nome, cliente.email, cliente.senha, cliente.id_cliente)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, id_cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        cursor.close()
        conn.close()


