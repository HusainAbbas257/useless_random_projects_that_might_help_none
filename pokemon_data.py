import csv, matplotlib.pyplot as plt
from collections import Counter

def load(file):
    with open(file) as f:
        return list(csv.DictReader(f))

def plot_scatter(data):
    types = list(set(t for p in data for t in p['types'].split(',')))
    cmap = {t:i for i,t in enumerate(types)}

    for t in types:
        subset = [p for p in data if t in p['types']]
        x = [int(p['height']) for p in subset]
        y = [int(p['weight']) for p in subset]
        plt.scatter(x,y,label=t,alpha=0.3)

    plt.legend(markerscale=2)
    plt.xlabel("Height"); plt.ylabel("Weight")
    plt.title("Height vs Weight by Type")
    plt.show()
def top_heavy(data):
    top = sorted(data, key=lambda p:int(p['weight']), reverse=True)[:10]
    plt.bar([p['name'] for p in top],[int(p['weight']) for p in top])
    plt.xticks(rotation=45)
    plt.title("Top 10 Heaviest")
    plt.show()
def plot_types(data):
    all_types = [t for p in data for t in p['types'].split(',')]
    c = Counter(all_types)
    plt.bar(c.keys(), c.values())
    plt.xticks(rotation=90)
    plt.title("Type Frequency")
    plt.show()

if __name__=="__main__":
    data = load('pokemons.csv')
    plot_scatter(data)
    top_heavy(data)
    plot_types(data)