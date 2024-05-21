from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Lista global para armazenar os Pokémons
pokemonList = []

def fetch_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    APIresponse = requests.get(url)
    if APIresponse.status_code == 200:
        data = APIresponse.json()
        return data['results']
    else:
        return []

def fetch_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    APIresponse = requests.get(url)
    if APIresponse.status_code == 200:
        data = APIresponse.json()
        abilities = [ability['ability']['name'] for ability in data['abilities'][:3]]
        return {
            'name': data['name'],
            'id': data['id'],
            'types': [type_data['type']['name'] for type_data in data['types']],
            'weight': data['weight'],
            'height': data['height'],
            'abilities': abilities,
            'image': data['sprites']['versions']['generation-v']['black-white']['animated']['front_default'],
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global pokemonList
    if not pokemonList:
        pokemonList = fetch_pokemon_list()
    
    pokemon_data = None
    if request.method == 'POST':
        pokemon_name = request.form['pokemon_name'].lower()
        pokemon_data = fetch_pokemon(pokemon_name)
    
    return render_template('index.html', pokemon=pokemon_data, pokemonList=pokemonList)

if __name__ == '__main__':
    app.run(debug=True)
