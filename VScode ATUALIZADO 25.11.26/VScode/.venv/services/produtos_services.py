##.venv\services\produtos_services.py
from config.db import criar_conexao


def list_produtos():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT codigo_produto, nome, descricao, preco, estoque
            FROM produto
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


def add_produto(nome: str, descricao: str, preco: float, estoque: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            INSERT INTO produto (nome, descricao, preco, estoque)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, descricao, preco, estoque))
        conn.commit()
        print("Produto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
    finally:
        cursor.close()
        conn.close()


def update_produto(codigo_produto: int, novo_preco: float, novo_estoque: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            UPDATE produto
            SET preco = %s, estoque = %s
            WHERE codigo_produto = %s
        """
        cursor.execute(sql, (novo_preco, novo_estoque, codigo_produto))
        conn.commit()
        print("Produto atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
    finally:
        cursor.close()
        conn.close()