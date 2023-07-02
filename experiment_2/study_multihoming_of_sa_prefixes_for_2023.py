import sys
import json
from infer_sa_prefixes import *

# Reads content from a json file
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# Writes content to a json file
def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)

def read_sa_prefixes(collection_year, peer):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    as_paths_per_origin = sa_prefixes['as_path_per_origin']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    return as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin

def is_customer_multihomed(AS_relationships_graph, customer):
    providers_or_peers = list(AS_relationships_graph.predecessors(customer))
    providers = [node for node in providers_or_peers if is_provider(AS_relationships_graph, customer, node)]
    print((customer, providers))
    num_of_providers = len(providers)
    return num_of_providers > 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Enter a year in range 2003-2023:')
        collection_year = input()
    else:
        collection_year = sys.argv[1]
    while int(collection_year) > 2023 and int(collection_year) < 2003:
        print('Enter a valid year (in the range 2003-2023):')
        collection_year = input()

    AS_relationships_graph = get_AS_relationships_graph('../__CAIDA_AS-graph__/' + collection_year + '0401.as-rel.txt')
    
    peers = ["3292", "3257", "3549", "5511", "7018"]
    
    as_paths_dict = dict()
    prefixes_dict = dict()
    sa_prefixes_dict = dict()
    multihoming_dict = dict()
    for peer in peers:
        as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin = read_sa_prefixes(
            collection_year, peer)
        as_paths_dict[peer] = as_paths_per_origin
        prefixes_dict[peer] = prefixes_per_origin
        sa_prefixes_dict[peer] = sa_customer_prefixes_per_origin
    
    
    for peer in peers:
        multihoming_dict[peer] = dict()
        multihoming_dict[peer]['multihomed_num'] = 0
        multihoming_dict[peer]['singlehomed_num'] = 0
        multihoming_dict[peer]['total'] = 0
        multihoming_dict[peer]['multihomed_ratio'] = 0
        multihoming_dict[peer]['singlehomed_ratio'] = 0

        for origin in sa_prefixes_dict[peer]:
            if is_customer_multihomed(AS_relationships_graph, origin):
                multihoming_dict[peer]['multihomed_num'] += 1
            else:
                multihoming_dict[peer]['singlehomed_num'] += 1
            multihoming_dict[peer]['total'] += 1
            multihoming_dict[peer]['multihomed_ratio'] = multihoming_dict[peer]['multihomed_num'] / \
                multihoming_dict[peer]['total']
            multihoming_dict[peer]['singlehomed_ratio'] = multihoming_dict[peer]['singlehomed_num'] / \
                multihoming_dict[peer]['total']

            

    print(multihoming_dict)




