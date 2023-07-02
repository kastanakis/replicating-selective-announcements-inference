import sys
import json
from pprint import pprint as pprint
import glob
import os

# Reads content from a json file
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# Writes content to a json file
def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)


def study_from_provider_pov(collection_year, peer):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    peer = sa_prefixes['peer']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    sa_peer_prefixes_per_origin = sa_prefixes['sa_peer_prefixes_per_origin']
    # Tables: % of customer SA prefixes in 2023, % of peer SA prefixes in 2023

    def flatten_list(list):
        return [val for sublist in list for val in sublist]
    percentage_of_sa_customer_prefixes = len(flatten_list(
        sa_customer_prefixes_per_origin.values())) / len(flatten_list(prefixes_per_origin.values()))
    percentage_of_sa_customer_origins = len(
        sa_customer_prefixes_per_origin.keys()) / len(prefixes_per_origin.keys())
    percentage_of_sa_peer_prefixes = len(flatten_list(
        sa_peer_prefixes_per_origin.values())) / len(flatten_list(prefixes_per_origin.values()))
    percentage_of_sa_peer_origins = len(
        sa_peer_prefixes_per_origin.keys()) / len(prefixes_per_origin.keys())
    return percentage_of_sa_customer_prefixes, percentage_of_sa_customer_origins, percentage_of_sa_peer_prefixes, percentage_of_sa_peer_origins, sa_prefixes


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Enter a year in range 2003-2023:')
        collection_year = input()
    else:
        collection_year = sys.argv[1]
    while int(collection_year) > 2023 and int(collection_year) < 2003:
        print('Enter a valid year (in the range 2003-2023):')
        collection_year = input()

    # ##################### ALL PEERS ############################
    peers = [x.split('sa_prefixes/' + collection_year + '/')[1].split('_')[0]
             for x in glob.glob('sa_prefixes/' + collection_year + '/*.json')]
    sa_peer_origin_announcement_ratio_per_provider = dict()
    sa_peer_prefix_announcement_ratio_per_provider = dict()
    for peer in peers:
        sa_customer_prefixes_ratio, sa_customer_origins_ratio, sa_peer_prefixes_ratio, sa_peer_origins_ratio, routing_table_metadata = study_from_provider_pov(
            collection_year, peer)
        sa_peer_prefix_announcement_ratio_per_provider[peer] = sa_peer_prefixes_ratio
        sa_peer_origin_announcement_ratio_per_provider[peer] = sa_peer_origins_ratio
    sorted_sa_origin_announcement_ratio_per_provider = dict(sorted(sa_peer_origin_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('export2peer/ratio_of_sa_origins.json', sorted_sa_origin_announcement_ratio_per_provider)
    sorted_sa_prefix_announcement_ratio_per_provider = dict(sorted(sa_peer_prefix_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('export2peer/ratio_of_sa_prefixes.json', sorted_sa_prefix_announcement_ratio_per_provider)
