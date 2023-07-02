import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

if __name__ == '__main__':
    peer = '7018'
    for month in range(0,12):
        to_write = dict()
        if month < 9:
            month += 1
            month = '0' + str(month)
        else:
            month += 1
            month = str(month)
        print(month)
        AS_relationships_graph = get_AS_relationships_graph('../__CAIDA_AS-graph__/2022' + month + '01.as-rel.txt')
        routing_table = '../data_collection/output/routing_tables/2022_AS7018/' + month + '_routing_table.csv'
        as_path_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin, sa_peer_prefixes_per_origin = collect_sa_prefixes(
            AS_relationships_graph, routing_table, peer)
        to_write['month'] = month
        to_write['as_path_per_origin'] = as_path_per_origin
        to_write['prefixes_per_origin'] = prefixes_per_origin
        to_write['sa_customer_prefixes_per_origin'] = sa_customer_prefixes_per_origin
        to_write['sa_peer_prefixes_per_origin'] = sa_peer_prefixes_per_origin
        write_json('sa_prefixes/2022_AS7018/' + month + '_sa_prefixes.json', to_write)
