import psycopg2
import os


def criar_conexao():

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432")
        )

        return conn

    except psycopg2.Error as e:
        print(f"Falha na conexão com o banco: {e}")
        return None
