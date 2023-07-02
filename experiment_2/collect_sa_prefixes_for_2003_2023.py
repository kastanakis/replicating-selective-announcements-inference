import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

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
    
    peers = [x.split('routing_tables/' + collection_year + '/')[1].split('_')[0]
             for x in glob.glob('../data_collection/output/routing_tables/' + collection_year + '/*.csv')]
    
    for peer in peers:
        to_write = dict()
        routing_table = '../data_collection/output/routing_tables/' + collection_year + '/' + peer + '_routing_table.csv'
        as_path_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin, sa_peer_prefixes_per_origin = collect_sa_prefixes(
            AS_relationships_graph, routing_table, peer)
        to_write['peer'] = peer
        to_write['as_path_per_origin'] = as_path_per_origin
        to_write['prefixes_per_origin'] = prefixes_per_origin
        to_write['sa_customer_prefixes_per_origin'] = sa_customer_prefixes_per_origin
        to_write['sa_peer_prefixes_per_origin'] = sa_peer_prefixes_per_origin
        write_json('sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json', to_write)
        
