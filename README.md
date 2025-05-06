# 🍿 Aplicação para Pesquisa de Filmes

- Aplicação desenvolvida para um trabalho proposto na disciplina de __Desenvolvimento Web III 💻__



## 🚨 Instalação

__1.  Clonar o repositório__
```
git clone https://github.com/joaovictormuraror/cinema-cache.git
```
__2. Criar um VENV__
```
python -m venv .venv
. .venv/bin/activate  # Mac
.venv\Scripts\activate  # Windows
```
__3. Intalar as dependências__
```
pip install flask
pip install psycopg['binary']
pip install requests
pip install jsonify
```
__4. Executar a aplicação__
```bash
flask --app app.py run --debug
```


## 🔎 Como pesquisar filmes/séries



          

No arquivo `requisicoes.http`, há os _GETs_ responsáveis por consultar o banco de dados e a API usada na aplicação.
> Para usar o requisições HTTP, deve estar instalado em seu __VSCode__, a extensão ___RestClient___

```
GET http://127.0.0.1:5000/search/title?titulo='nomedofilme'
```
- Substitua o `nomedofilme` pelo filme que você deseja buscar (sem as aspas). A requisição irá retornar os dados sobre o filme/série desejado

```
GET http://127.0.0.1:5000/movies
```
- A requisição irá mostrar os filmes/séries já pesquisados anteriormente, pois eles estarão armazenados em um banco de dados
