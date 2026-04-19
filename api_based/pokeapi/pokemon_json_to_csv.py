import json,csv
import api_based.pokeapi.pokemon as pokemon
pokemons=pokemon.list_pokemons()
with open('pokemons.csv','w',newline='') as csvfile:
    fieldnames=['id','name','height','weight','types']
    writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()
    for pokemon_name in pokemons:
        try:
            with open(f'pokemons/{pokemon_name}.json','r') as f:
                data=json.load(f)
                types=[t['type']['name'] for t in data['types']]
                writer.writerow({
                    'id':data['id'],
                    'name':data['name'],
                    'height':data['height'],
                    'weight':data['weight'],
                    'types':','.join(types)
                })
        except FileNotFoundError:
            print(f'JSON file for {pokemon_name} not found.')
