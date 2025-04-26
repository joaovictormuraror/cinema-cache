import psycopg
from config import DATABASE_URL

conn = psycopg.connect(DATABASE_URL)
conn.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        imdb_id TEXT UNIQUE,
        title TEXT,
        year TEXT,
        type TEXT,
        data JSONB
    );
""")
conn.commit()

def buscar_por_titulo(titulo):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM movies WHERE title = %s", (titulo,))
        return cur.fetchone()

def buscar_por_id(imdb_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM movies WHERE imdb_id = %s", (imdb_id,))
        return cur.fetchone()

def inserir_filme(filme):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO movies (imdb_id, title, year, type, data)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (imdb_id) DO NOTHING
        """, (filme["imdbID"], filme["Title"], filme["Year"], filme["Type"], filme))
    conn.commit()