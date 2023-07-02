import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

def read_sa_prefixes(collection_year, peer):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    as_paths_per_origin = sa_prefixes['as_path_per_origin']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    return as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin

def is_customer_path(G, path):
    return is_provider(G, path[1], path[0])
    
def indirect_customer_path_to_origin_exists(as_paths_dict, origin):
    for peer in as_paths_dict:
        if origin not in as_paths_dict[peer]:
            continue
        for path in as_paths_dict[peer][origin]:
            # if len(path) < 3: continue
            if is_customer_path(AS_relationships_graph, path):
                return True
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Enter a year in range 2003-2023:')
        collection_year = input()
    else:
        collection_year = sys.argv[1]
    while int(collection_year) > 2023 and int(collection_year) < 2003:
        print('Enter a valid year (in the range 2003-2023):')
        collection_year = input()

    AS_relationships_graph = get_AS_relationships_graph(
            '../__CAIDA_AS-graph__/' + collection_year + '0401.as-rel.txt')
    
    peers = [x.split('sa_prefixes/' + collection_year + '/')[1].split('_')[0]
             for x in glob.glob('sa_prefixes/' + collection_year + '/*.json')]
    
    print(peers)
    as_paths_dict = dict()
    prefixes_dict = dict()
    sa_prefixes_dict = dict()
    active_sa_prefixes_ratio = dict()
    for peer in peers:
        active_sa_prefixes_ratio[peer] = [0, 0]
        as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin = read_sa_prefixes(
            collection_year, peer)
        as_paths_dict[peer] = as_paths_per_origin
        prefixes_dict[peer] = prefixes_per_origin
        sa_prefixes_dict[peer] = sa_customer_prefixes_per_origin
    
    for peer in peers:
        denominator = 0
        for origin in sa_prefixes_dict[peer]:
            if origin in as_paths_dict[peer]:
                denominator += 1
            else:
                continue
            if indirect_customer_path_to_origin_exists(as_paths_dict, origin):
                active_sa_prefixes_ratio[peer][0] += 1
        if denominator: active_sa_prefixes_ratio[peer][0] /= denominator
        active_sa_prefixes_ratio[peer][1] = denominator

    verification_sorted = dict(
        sorted(active_sa_prefixes_ratio.items(), key=lambda x: x[1][0], reverse=True))
    write_json('verification/' + collection_year + '_verification_ratio_per_provider.json', verification_sorted)
