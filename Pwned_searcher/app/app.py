from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def search_solr(field, term):
    solr_url = "http://localhost:8983/solr/searcher/select"
    params = {
        "q": f"{field}:{term}",
        "wt": "json"
    }

    response = requests.get(solr_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'response' in data and 'docs' in data['response'] and data['response']['docs']:
            return data['response']['docs']
        else:
            return None
    else:
        return None
    
@app.route('/')
def index():
    response = requests.get('http://localhost:8983/solr/searcher/select', params={
        'q': '*:*',
        'rows': 0
    })
    num_docs = format(int(response.json()['response']['numFound']), ',')
    return render_template('index.html', num_docs=num_docs)

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['searchType']
    search_term = request.form['searchTerm']
    
    if search_type == 'username':
        results = search_solr('Username', f'"{search_term}"')
    elif search_type == 'email':
        results = search_solr('Email', search_term)
    elif search_type == 'ip':
        results = search_solr('Ip', search_term)
    else:
        return jsonify(error="Type de recherche invalide")

    if results:
        return jsonify(results=results)
    else:
        return jsonify(error=f"Aucun résultat trouvé pour {search_type} : {search_term}.")
app.run(debug=True)