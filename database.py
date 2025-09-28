import sqlite3

DATABASE = 'recortes_producao.db'

def connect_db():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

def init_db():
    """Inicializa o banco de dados e cria a tabela 'recortes' se não existir."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recortes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_peca TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                medidaa INTEGER NOT NULL,
                medidab INTEGER NOT NULL,
                data_producao TEXT NOT NULL,
                turno TEXT NOT NULL,
                observacoes TEXT
            )
        ''')
        conn.commit()
    print("Banco de dados inicializado.")

if __name__ == '__main__':
    init_db()
    print("Execute 'python database.py' uma vez para criar o banco de dados.")
