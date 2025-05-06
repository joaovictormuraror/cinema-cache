import os
import psycopg

import json

URL_BANCO_DADOS = "postgresql://postgres:3f%40db@164.90.152.205:80/poliqueta"
CHAVE_API_OMDB = "fd8f2f01"
URL_API_OMDB = "http://www.omdbapi.com/"

conexao = psycopg.connect(URL_BANCO_DADOS)
conexao.execute("""
    CREATE TABLE IF NOT EXISTS filmes (
        id SERIAL PRIMARY KEY,
        imdb_id TEXT UNIQUE,
        titulo TEXT,
        ano TEXT,
        tipo TEXT,
        data JSONB
    );
""")
conexao.commit()

def buscar_filme_titulo(titulo):
    with conexao.cursor() as cur:
        cur.execute("SELECT * FROM filmes WHERE titulo = %s", (titulo,))
        return cur.fetchone()

def buscar_filme_id(imdb_id):
    with conexao.cursor() as cur:
        cur.execute("SELECT * FROM filmes WHERE id_imdb = %s", (imdb_id,))
        return cur.fetchone()


def salvar_filme(filme):
    with conexao.cursor() as cur:
        cur.execute("""
            INSERT INTO filmes (id_imdb, titulo, ano, tipo, data)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_imdb) DO NOTHING
        """, (
            filme.get("imdbID"),
            filme.get("Title"),
            filme.get("Year"),
            filme.get("Type"),
            json.dumps(filme)
        ))