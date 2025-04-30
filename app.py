from flask import Flask, request, jsonify
import requests
import banco_dados as db
from config import CHAVE_API_OMDB, URL_API_OMDB

app = Flask(__name__)

def buscar_no_omdb(parametros):
    parametros['apikey'] = CHAVE_API_OMDB
    resposta = requests.get(URL_API_OMDB, params=parametros)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados.get("Response") == "True":
            return dados
    return None

@app.route('/movies', methods=['GET'])
def listar_filmes():
    with db.conexao.cursor() as cur:
        cur.execute("SELECT titulo FROM filmes")
        filmes = cur.fetchall()
    return jsonify([f[0] for f in filmes])

@app.route('/search/title', methods=['GET'])
def buscar_por_titulo():
    titulo = request.args.get('titulo')
    if not titulo:
        return jsonify({'error': 'Título obrigatório'}), 400

    dados_local = db.buscar_filme_titulo(titulo)
    if dados_local:
        return jsonify(dados_local[5]) 

    dados_externos = buscar_no_omdb({'t': titulo})
    if dados_externos:
        db.salvar_filme(dados_externos)
        return jsonify(dados_externos)

    return jsonify({'error': 'Filme não encontrado'}), 404

@app.route('/search/id', methods=['GET'])
def buscar_por_id():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'ID obrigatório'}), 400

    dados_local = db.buscar_filme_id(imdb_id)  # Corrigido
    if dados_local:
        return jsonify(dados_local[5])  # índice do campo JSONB

    dados_externos = buscar_no_omdb({'i': imdb_id})
    if dados_externos:
        db.salvar_filme(dados_externos)
        return jsonify(dados_externos)

    return jsonify({'error': 'Filme não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)