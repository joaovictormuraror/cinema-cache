from flask import Flask, request, jsonify
import requests
import banco_dados as db
from config import OMDB_API_KEY, OMDB_API_URL

app = Flask(__name__)

def fetch_from_omdb(params):
    params['apikey'] = OMDB_API_KEY
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
    return None

@app.route('/movies', methods=['GET'])
def listar_filmes():
    with db.conn.cursor() as cur:
        cur.execute("SELECT title FROM movies")
        movies = cur.fetchall()
    return jsonify(movies)

@app.route('/search/title', methods=['GET'])
def buscar_por_titulo():
    titulo = request.args.get('title')
    if not titulo:
        return jsonify({'error': 'Title is required'}), 400

    local_data = db.buscar_por_titulo(titulo)  # Corrigido
    if local_data:
        return jsonify(local_data[5])  # índice do campo JSONB

    external_data = fetch_from_omdb({'t': titulo})
    if external_data:
        db.inserir_filme(external_data)
        return jsonify(external_data)

    return jsonify({'error': 'Movie not found'}), 404

@app.route('/search/id', methods=['GET'])
def buscar_por_id():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'ID is required'}), 400

    local_data = db.buscar_por_id(imdb_id)  # Corrigido
    if local_data:
        return jsonify(local_data[5])  # índice do campo JSONB

    external_data = fetch_from_omdb({'i': imdb_id})
    if external_data:
        db.inserir_filme(external_data)
        return jsonify(external_data)

    return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)