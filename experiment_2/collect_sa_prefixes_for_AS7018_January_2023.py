import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

if __name__ == '__main__':
    AS_relationships_graph = get_AS_relationships_graph('../__CAIDA_AS-graph__/20230201.as-rel.txt')
    peer = '7018'
    for day in range(0,31):
        to_write = dict()
        if day < 9:
            day += 1
            day = '0' + str(day)
        else:
            day += 1
            day = str(day)
        print(day)
        routing_table = '../data_collection/output/routing_tables/2023_January_AS7018/' + day + '_routing_table.csv'
        as_path_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin, sa_peer_prefixes_per_origin = collect_sa_prefixes(
            AS_relationships_graph, routing_table, peer)
        to_write['day'] = day
        to_write['as_path_per_origin'] = as_path_per_origin
        to_write['prefixes_per_origin'] = prefixes_per_origin
        to_write['sa_customer_prefixes_per_origin'] = sa_customer_prefixes_per_origin
        to_write['sa_peer_prefixes_per_origin'] = sa_peer_prefixes_per_origin
        write_json('sa_prefixes/2023_January_AS7018/' + day + '_sa_prefixes.json', to_write)
