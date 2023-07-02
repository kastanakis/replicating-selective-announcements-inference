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

def intersection_of_providers_in_twenty_years():
    # specify the directory path
    dir_path = "sa_prefixes/"

    # get a list of all the subdirectories
    subdirs = [f.path for f in os.scandir(dir_path) if f.is_dir() and 'AS7018' not in f.path]
    print(subdirs)
    # initialize the set of filenames for the first subdirectory
    first_subdir_files = set(os.listdir(subdirs[0]))

    # loop through the remaining subdirectories and take the intersection of their filenames
    for subdir in subdirs[1:]:
        subdir_files = set(os.listdir(subdir))
        first_subdir_files.intersection_update(subdir_files)
    
    providers = list()
    for file in first_subdir_files:
        providers.append(file.split('_sa_prefixes.json')[0])
    return providers

def study_from_provider_pov(collection_year, peer):
    to_write = dict()
    sa_prefixes = read_json('sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    peer = sa_prefixes['peer']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    sa_peer_prefixes_per_origin = sa_prefixes['sa_peer_prefixes_per_origin']
    # Tables: % of customer SA prefixes in 2023, % of peer SA prefixes in 2023
    def flatten_list(list):
        return [val for sublist in list for val in sublist]
    percentage_of_sa_customer_prefixes = len(flatten_list(sa_customer_prefixes_per_origin.values())) / len(flatten_list(prefixes_per_origin.values()))
    percentage_of_sa_customer_origins = len(
        sa_customer_prefixes_per_origin.keys()) / len(prefixes_per_origin.keys())
    percentage_of_sa_peer_origins = len(
        sa_peer_prefixes_per_origin.keys()) / len(prefixes_per_origin.keys())
    return percentage_of_sa_customer_prefixes, percentage_of_sa_customer_origins, percentage_of_sa_peer_origins, sa_prefixes

def get_common_direct_or_indirect_customers(selected_peers, routing_table_metadata_dict):
    common_customers = set()
    for peer in selected_peers:
        if not common_customers:
            common_customers = set(
                routing_table_metadata_dict[peer]['prefixes_per_origin'].keys())
        else:
            common_customers = common_customers.intersection(
                routing_table_metadata_dict[peer]['prefixes_per_origin'].keys())
    return common_customers

def get_all_direct_or_indirect_customers(selected_peers, routing_table_metadata_dict):
    all_customers = set()
    for peer in selected_peers:
        if not all_customers:
            all_customers = set(
                routing_table_metadata_dict[peer]['prefixes_per_origin'].keys())
        else:
            all_customers = all_customers.union(
                routing_table_metadata_dict[peer]['prefixes_per_origin'].keys())
    return all_customers

def study_from_customer_pov(peer, customer, routing_table_metadata_dict):
    if customer not in routing_table_metadata_dict[peer]['sa_customer_prefixes_per_origin']:
        prefixes = []
        sa_prefixes = []
    else:
        prefixes = routing_table_metadata_dict[peer]['prefixes_per_origin'][customer]
        sa_prefixes = routing_table_metadata_dict[peer]['sa_customer_prefixes_per_origin'][customer]
    return prefixes, sa_prefixes  


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
    sa_origin_announcement_ratio_per_provider = dict()
    sa_prefix_announcement_ratio_per_provider = dict()
    routing_table_metadata_dict = dict()
    for peer in peers:
        sa_customer_prefixes_ratio, sa_customer_origins_ratio, sa_peer_ratio, routing_table_metadata = study_from_provider_pov(
            collection_year, peer)
        sa_origin_announcement_ratio_per_provider[peer] = sa_customer_origins_ratio
        sa_prefix_announcement_ratio_per_provider[peer] = sa_customer_prefixes_ratio
        routing_table_metadata_dict[peer] = routing_table_metadata
    sorted_sa_origin_announcement_ratio_per_provider = dict(
        sorted(sa_origin_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/all_peers_per_year_' + collection_year +
               '_ratio_of_sa_origin_announcements_from_the_provider_pov.json', sorted_sa_origin_announcement_ratio_per_provider)
    sorted_sa_prefix_announcement_ratio_per_provider = dict(
        sorted(sa_prefix_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/all_peers_per_year_' + collection_year + '_ratio_of_sa_prefix_announcements_from_the_provider_pov.json',
               sorted_sa_prefix_announcement_ratio_per_provider)

    ##################### INTERSECTION PEERS ############################
    selected_peers = intersection_of_providers_in_twenty_years()
    sa_origin_announcement_ratio_per_provider = dict()
    sa_prefix_announcement_ratio_per_provider = dict()
    for peer in selected_peers:
        sa_customer_prefixes_ratio, sa_customer_origins_ratio, sa_peer_ratio, routing_table_metadata = study_from_provider_pov(
            collection_year, peer)
        sa_origin_announcement_ratio_per_provider[peer] = sa_customer_origins_ratio
        sa_prefix_announcement_ratio_per_provider[peer] = sa_customer_prefixes_ratio
    sorted_sa_origin_announcement_ratio_per_provider = dict(
        sorted(sa_origin_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/intersection_of_peers_20_years_' + collection_year +
               '_ratio_of_sa_origin_announcements_from_the_provider_pov.json', sorted_sa_origin_announcement_ratio_per_provider)
    sorted_sa_prefix_announcement_ratio_per_provider = dict(
        sorted(sa_prefix_announcement_ratio_per_provider.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/intersection_of_peers_20_years_' + collection_year + '_ratio_of_sa_prefix_announcements_from_the_provider_pov.json',
               sorted_sa_prefix_announcement_ratio_per_provider)

    ##################### INTERSECTION OF CUSTOMERS OF INTERSECTION OF PEERS ############################
    common_customers = get_common_direct_or_indirect_customers(
        selected_peers, routing_table_metadata_dict)
    sa_announcement_ratio_per_customer = dict()
    for customer in common_customers:
        SA_prefixes = set()
        all_prefixes = set()
        for peer in selected_peers:
            prefixes, sa_prefixes = study_from_customer_pov(
                peer, customer, routing_table_metadata_dict)
            for prefix in prefixes:
                all_prefixes.add(prefix)
            for sa_prefix in sa_prefixes:
                SA_prefixes.add(sa_prefix)
            
        if(len(all_prefixes) > 10):
            average_sa_ratio = (len(SA_prefixes)/len(all_prefixes))
            sa_announcement_ratio_per_customer[customer] = average_sa_ratio
        
    sorted_sa_announcement_ratio_per_customer = dict(sorted(sa_announcement_ratio_per_customer.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/intersection_of_customers_for_intersection_of_peers_' + collection_year +
               '_ratio_of_sa_announcements_from_the_customer_pov.json', sorted_sa_announcement_ratio_per_customer)
    
    ##################### UNION OF CUSTOMERS OF ALL PEERS PER YEAR ############################
    all_customers = get_all_direct_or_indirect_customers(
        peers, routing_table_metadata_dict)
    sa_announcement_ratio_per_customer = dict()
    for customer in all_customers:
        SA_prefixes = set()
        all_prefixes = set()
        for peer in peers:
            prefixes, sa_prefixes = study_from_customer_pov(
                peer, customer, routing_table_metadata_dict)
            for prefix in prefixes:
                all_prefixes.add(prefix)
            for sa_prefix in sa_prefixes:
                SA_prefixes.add(sa_prefix)

        if(len(all_prefixes) > 10):
            average_sa_ratio = (len(SA_prefixes)/len(all_prefixes))
            sa_announcement_ratio_per_customer[customer] = average_sa_ratio

    sorted_sa_announcement_ratio_per_customer = dict(sorted(
        sa_announcement_ratio_per_customer.items(), key=lambda x: x[1], reverse=True))
    write_json('prevalence/' + collection_year + '/union_of_customers_for_all_providers_' + collection_year +
                '_ratio_of_sa_announcements_from_the_customer_pov.json', sorted_sa_announcement_ratio_per_customer)

