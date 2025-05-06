from flask import Flask, request, jsonify
import requests
import banco_dados as db


URL_BANCO_DADOS = "postgresql://postgres:3f%40db@164.90.152.205:80/poliqueta"
CHAVE_API_OMDB = "fd8f2f01"
URL_API_OMDB = "http://www.omdbapi.com/"

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
        return jsonify({'error': 'Título obrigatório'})

    dados_local = db.buscar_filme_titulo(titulo)
    if dados_local:
        return jsonify(dados_local[5]) 

    dados_externos = buscar_no_omdb({'t': titulo})
    if dados_externos:
        db.salvar_filme(dados_externos)
        return jsonify(dados_externos)

    return jsonify({'error': 'Filme não encontrado'})

@app.route('/search/id', methods=['GET'])
def buscar_por_id():
    imdb_id = request.args.get('id')
    if not imdb_id:
        return jsonify({'error': 'ID obrigatório'})

    dados_local = db.buscar_filme_id(imdb_id)
    if dados_local:
        return jsonify(dados_local[5])

    dados_externos = buscar_no_omdb({'i': imdb_id})
    if dados_externos:
        db.salvar_filme(dados_externos)
        return jsonify(dados_externos)

    return jsonify({'error': 'Filme nao encontrado'})

if __name__ == '__main__':
    app.run(debug=True)