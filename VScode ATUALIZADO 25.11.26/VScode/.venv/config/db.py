##.venv\config\db.py
import psycopg2

def criar_conexao():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='localhost',
            password='senha', ##Digite a senha que você colocou no Dbeaver
            port='5432'
        )
        ##print ("A conexão foi realizada com sucesso") apenas ver se conectou
        return conn
    except Exception as e:
        print(f"A conexão falhou!\nCodigo de erro {e}")