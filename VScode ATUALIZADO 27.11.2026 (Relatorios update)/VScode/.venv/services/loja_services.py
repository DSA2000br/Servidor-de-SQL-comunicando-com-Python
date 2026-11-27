##.venv\services\loja_services.py
from config.db import criar_conexao


def listar_produtos():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT codigo_produto, nome, descricao, preco, estoque
            FROM produto
            WHERE estoque > 0
            ORDER BY codigo_produto
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def buscar_produto(codigo_produto: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT codigo_produto, nome, descricao, preco, estoque
            FROM produto
            WHERE codigo_produto = %s
        """
        cursor.execute(sql, (codigo_produto,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def listar_compras_cliente(codigo_cliente: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT
                v.numero_venda,
                v.data_venda,
                p.nome AS produto,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario) AS subtotal_item,
                v.valor_total
            FROM venda v
            INNER JOIN item_venda iv ON v.numero_venda = iv.numero_venda
            INNER JOIN produto p ON iv.codigo_produto = p.codigo_produto
            WHERE v.codigo_cliente = %s
            ORDER BY v.numero_venda DESC, p.nome
        """
        cursor.execute(sql, (codigo_cliente,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar historico de compras: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def _obter_funcionario_padrao(cursor) -> int:
    cursor.execute("""
        SELECT id
        FROM cliente
        WHERE LOWER(TRIM(cargo)) IN ('administrador', 'funcionario', 'funcionário')
        ORDER BY id
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute("SELECT id FROM cliente ORDER BY id LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else 1


def finalizar_compra(codigo_cliente: int, carrinho: list, codigo_funcionario: int | None = None):
    """
    carrinho: lista de dicionarios com chaves:
    {'codigo_produto': int, 'nome': str, 'quantidade': int, 'preco_unitario': float}
    """
    if not carrinho:
        print("Seu carrinho esta vazio!")
        return False

    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        if codigo_funcionario is None:
            codigo_funcionario = _obter_funcionario_padrao(cursor)

        valor_total = sum(item["quantidade"] * item["preco_unitario"] for item in carrinho)

        cursor.execute("SELECT COALESCE(MAX(numero_venda), 1000) + 1 FROM venda")
        numero_venda = cursor.fetchone()[0]

        sql_venda = """
            INSERT INTO venda (numero_venda, valor_total, codigo_cliente, codigo_funcionario)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_venda, (numero_venda, valor_total, codigo_cliente, codigo_funcionario))

        sql_item = """
            INSERT INTO item_venda (numero_venda, codigo_produto, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s)
        """
        sql_estoque = """
            UPDATE produto
            SET estoque = estoque - %s
            WHERE codigo_produto = %s AND estoque >= %s
        """

        for item in carrinho:
            cursor.execute(
                sql_item,
                (numero_venda, item["codigo_produto"], item["quantidade"], item["preco_unitario"]),
            )
            cursor.execute(
                sql_estoque,
                (item["quantidade"], item["codigo_produto"], item["quantidade"]),
            )
            if cursor.rowcount == 0:
                raise Exception(f"Estoque insuficiente para o produto {item['nome']}")

        conn.commit()
        print(f"Compra finalizada com sucesso! Numero da venda: {numero_venda} | Total: R$ {valor_total:.2f}")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao finalizar compra: {e}")
        return False
    finally:
        cursor.close()
        conn.close()