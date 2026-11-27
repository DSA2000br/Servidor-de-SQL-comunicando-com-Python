##.venv\services\User_services.py
from config.db import criar_conexao
from config.crypt import criptografar, verificar_senha

def import_user(nome: str, email: str, senha: str, telefone: str, endereco: str, cpf: str, cargo: str = "Cliente"):
    conn = None
    cursor = None
    try:
        conn = criar_conexao()
        if conn is None:
         return
        cursor = conn.cursor()

        senha_hash = criptografar(senha)

        sql = """
            INSERT INTO cliente (nome, email, senha, telefone, endereco, cpf, cargo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, email, senha, telefone, endereco, cpf, cargo))
        conn.commit()
        print(f"Conta ({cargo}) cadastrada com sucesso")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao cadastrar conta: {e}")
    finally:
     if cursor:
        cursor.close()
     if conn:
        conn.close()


def login(email: str, senha: str):
    conn = None
    cursor = None

    try:
        conn = criar_conexao()
        if conn is None:
         return None
        cursor = conn.cursor()
        sql = "SELECT * FROM cliente WHERE email = %s AND senha = %s"
        cursor.execute(sql, (email, senha))
        user = cursor.fetchone()

        if user is None:
            return None
        
        colunas = [col[0] for col in cursor.description]
        indice_senha = colunas.index("senha")

        senha_hash = user[indice_senha]

        if verificar_senha(senha, senha_hash):
         return user
        
        return None
    
    except Exception as e:
        print(f"Erro no login: {e}")
        return None
    finally:
     if cursor:
      cursor.close()
     if conn:
      conn.close()


def list_users():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = """
            SELECT id, nome, email, telefone, cargo
            FROM cliente
            ORDER BY id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar contas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id: int, current_user_id: int):
    if user_id == current_user_id:
        print("  [!] Voce nao pode deletar a conta que esta usando agora.")
        return

    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        cursor.execute("SELECT nome, cargo FROM cliente WHERE id = %s", (user_id,))
        alvo = cursor.fetchone()
        if not alvo:
            print("  [!] Nenhuma conta encontrada com esse ID.")
            return

        nome_alvo, cargo_alvo = alvo[0] or "", (alvo[1] or "").strip().lower()
        if user_id == 5 or (cargo_alvo == "administrador" and "daniel" in nome_alvo.lower()):
            print("  [!] Esse ADM, não pode ser deletado, ele é o dono")
            return

        sql = "DELETE FROM cliente WHERE id = %s"
        cursor.execute(sql, (user_id,))
        if cursor.rowcount == 0:
            print("  [!] Nenhuma conta encontrada com esse ID.")
            conn.rollback()
        else:
            conn.commit()
            print("  Conta removida com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"  [!] Nao foi possivel deletar a conta (ela pode estar vinculada a tarefas ou vendas): {e}")
    finally:
        cursor.close()
        conn.close()