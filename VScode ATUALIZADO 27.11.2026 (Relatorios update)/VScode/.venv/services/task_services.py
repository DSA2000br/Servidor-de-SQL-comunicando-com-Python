##.venv\services\task_services.py
from config.db import criar_conexao


# ---------- CRUD TASK ----------
def create_task(user_id: int, title: str):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "INSERT INTO task (tittle, user_id) VALUES (%s, %s)"
        cursor.execute(sql, (title, user_id))
        conn.commit()
        print("Task cadastrada")
    except Exception as e:
        print(f"Erro ao cadastrar task: {e}")
    finally:
        cursor.close()
        conn.close()


def search_tasks(user_id: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "SELECT id, tittle, user_id FROM task WHERE user_id = %s ORDER BY id"
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar tasks: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def update_task(task_id: int, new_title: str):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "UPDATE task SET tittle = %s WHERE id = %s"
        cursor.execute(sql, (new_title, task_id))
        conn.commit()
        print("Task atualizada")
    except Exception as e:
        print(f"Erro ao atualizar task: {e}")
    finally:
        cursor.close()
        conn.close()


def remove_task(task_id: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "DELETE FROM task WHERE id = %s"
        cursor.execute(sql, (task_id,))
        conn.commit()
        print("Task removida")
    except Exception as e:
        print(f"Erro ao remover task: {e}")
    finally:
        cursor.close()
        conn.close()


# ---------- JOINS / RELATORIOS ----------
def join_vendas_cliente_funcionario():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                v.numero_venda,
                v.data_venda,
                v.valor_total,
                c.nome AS nome_cliente,
                c.cargo AS cargo_cliente
            FROM venda v
            INNER JOIN cliente c ON v.codigo_cliente = c.id
            ORDER BY v.numero_venda
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro no relatorio de vendas e clientes: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def join_itens_venda_detalhados():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                v.numero_venda,
                c.nome AS cliente,
                p.nome AS produto,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario) AS subtotal_item
            FROM item_venda iv
            INNER JOIN venda v ON iv.numero_venda = v.numero_venda
            INNER JOIN cliente c ON v.codigo_cliente = c.id
            INNER JOIN produto p ON iv.codigo_produto = p.codigo_produto
            ORDER BY v.numero_venda, p.nome
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro no relatorio de itens de venda: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def join_clientes_e_tasks():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                c.id,
                c.nome AS cliente,
                c.cargo,
                t.id AS id_task,
                COALESCE(t.tittle, 'Sem tarefa cadastrada') AS tarefa
            FROM cliente c
            LEFT JOIN task t ON c.id = t.user_id
            ORDER BY c.id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro no relatorio de clientes e tasks: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def join_vendas_por_funcionario():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                c.id,
                c.nome AS usuario,
                c.cargo,
                COUNT(v.numero_venda) AS total_compras,
                COALESCE(SUM(v.valor_total), 0) AS total_gasto
            FROM cliente c
            LEFT JOIN venda v ON c.id = v.codigo_cliente
            WHERE LOWER(TRIM(c.cargo)) <> 'cliente'
            GROUP BY c.id, c.nome, c.cargo
            ORDER BY total_gasto DESC, c.id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro no relatorio de compras por usuario: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def join_itens_com_cliente():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                v.numero_venda,
                c.id AS cliente_id,
                c.nome AS cliente_nome,
                c.cargo AS cliente_cargo,
                p.nome AS item_nome,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario) AS subtotal_item
            FROM item_venda iv
            INNER JOIN venda v ON iv.numero_venda = v.numero_venda
            INNER JOIN cliente c ON v.codigo_cliente = c.id
            INNER JOIN produto p ON iv.codigo_produto = p.codigo_produto
            ORDER BY v.numero_venda, p.nome
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro no relatorio de itens e clientes: {e}")
        return []
    finally:
        cursor.close()
        conn.close()