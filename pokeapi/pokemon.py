import requests
import json
base=r'https://pokeapi.co/api/v2/'
def get_pokemon(pokemon):
    # check in pokemons folder first
    try:
        with open(f'pokemons/{pokemon}.json','r') as f:
            data=json.load(f)
            print('Pokemon found in local storage:')
            print(f"{data['id']}: {data['name'].capitalize()}")
            return
    except FileNotFoundError:
        print('Pokemon not found in local storage. getting from API...')
    response=requests.get(base+'pokemon/'+pokemon)
    if response.status_code==200:
        data=response.json()
        print(f"{data['id']}: {data['name'].capitalize()}")
        with open(f'pokemons/{data["name"]}.json','w') as f:
            json.dump(data,f,indent=4)
    else:
        print('Pokemon not found.')
def list_pokemons():
    response=requests.get(base+'pokemon?limit=1000')
    if response.status_code==200:
        data=response.json()
        pokemons=[pokemon['name'] for pokemon in data['results']]
        print('Available Pokemons:')
        for pokemon in pokemons:
            print(pokemon)
        return pokemons
    else:
        print('Failed to retrieve Pokemon list.')
def initialize_storage():
    for i in range(1, 1009):
        get_pokemon(str(i))
if __name__=="__main__":
    #initialize_storage() # Uncomment to fetch and store all Pokemon data
    print('1-Search for a specific Pokemon')
    print('2.List all available Pokemons')
    choice=input('Enter your choice (1 or 2): ')
    if choice=='1':
        pokemon=input('Enter a Pokemon name: ')
        get_pokemon(pokemon.lower())
    elif choice=='2':
        list_pokemons()
    else:
        print('invalid choice.')    