import os
from flask import Flask, render_template, request, jsonify
from scholarly import scholarly

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    dados = request.get_json() or {}
    tema = dados.get('tema', '').strip()
    
    if not tema:
        return jsonify({'erro': 'Por favor, informe um tema válido.'}), 400

    try:
        # Busca no Google Acadêmico
        search_query = scholarly.search_pubs(tema)
        resultados = []

        # Tenta obter até 10 resultados
        for _ in range(10):
            try:
                artigo = next(search_query)
                bib = artigo.get('bib', {})
                
                link_pdf = artigo.get('eprint_url', None)
                link_pub = artigo.get('pub_url', '#')

                resultados.append({
                    'titulo': bib.get('title', 'Sem título'),
                    'autores': bib.get('author', ['Autor não informado']),
                    'ano': bib.get('pub_year', 'N/A'),
                    'resumo': bib.get('abstract', 'Sem resumo disponível.'),
                    'link_artigo': link_pub,
                    'link_pdf': link_pdf
                })
            except StopIteration:
                break

        return jsonify({'sucesso': True, 'resultados': resultados})

    except Exception as e:
        return jsonify({'erro': f'Erro ao processar a pesquisa: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
