import json
import glob
from pprint import pprint as pprint
import matplotlib.pyplot as plt


def plot_incremental_prefixes(sa_prefixes):
    x = []
    y = []

    unique_prefixes = set()

    for as_number, prefixes in sa_prefixes.items():
        unique_prefixes.update(prefixes)
        x.append(as_number)
        y.append(len(unique_prefixes))

    plt.plot(x, y, marker='o')
    plt.xlabel('AS Numbers')
    plt.ylabel('Total Unique Prefixes')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("unique_sa_prefixes.png")


# Reads content from a json file
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)


def flatten_list(list):
    return [val for sublist in list for val in sublist]


def extract_sa_prefixes_per_peer(collection_year, peer):
    sa_prefixes = read_json('../experiment_2/sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    sa_prefixes = flatten_list(sa_customer_prefixes_per_origin.values())

    return sa_prefixes


if __name__ == '__main__':
    collection_year = '2023'
    peers = [x.split('../experiment_2/sa_prefixes/' + collection_year + '/')[1].split('_')[0]
             for x in glob.glob('../experiment_2/sa_prefixes/' + collection_year + '/*.json')]
    sa_prefixes_per_peer = dict()
    for peer in peers:
        sa_prefixes_per_peer[peer] = extract_sa_prefixes_per_peer(collection_year, peer)
    
    plot_incremental_prefixes(sa_prefixes_per_peer)
        
