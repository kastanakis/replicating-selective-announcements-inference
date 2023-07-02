import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

def find_aggregatable_sa_prefixes(all_prefixes_difference_sa_prefixes_per_origin, sa_prefixes_per_origin):
    # convert the list of IP prefixes to a set of IP networks
    all_ip_networks = set(ipaddress.ip_network(prefix)
                          for prefix in all_prefixes_difference_sa_prefixes_per_origin)
    sa_ip_networks = set(ipaddress.ip_network(prefix)
                         for prefix in sa_prefixes_per_origin)
    # create a list to store the aggregatable prefixes
    aggregatable_prefixes = set()
    # iterate through the list of SA IP networks
    for prefix in sa_ip_networks:
        # iterate through the set of all IP networks to find which SA prefixes can be aggregated by at least one of all IP networks
        broken = 0
        for other_prefix in all_ip_networks:
            if other_prefix.version == prefix.version and other_prefix != prefix and prefix.subnet_of(other_prefix):
                # prefix is aggregated by other_prefix that happens because the provider doesnt want to propagate a 
                # favorable customer path for a customer prefix, hence it aggregates it to its own less specific prefix and 
                # announces that using a customer path and the more specific through a peer link. If the 'prefix' can be aggregated
                # by 'other_prefix' then the sa prefix is aggregatable.
                broken = 1
                break
        if broken:
            aggregatable_prefixes.add(prefix)
    # return the split sa prefixes
    return aggregatable_prefixes

def find_split_sa_prefixes(all_prefixes_difference_sa_prefixes_per_origin, sa_prefixes_per_origin):
    # convert the list of IP prefixes to a set of IP networks
    all_ip_networks = set(ipaddress.ip_network(prefix) for prefix in all_prefixes_difference_sa_prefixes_per_origin)
    sa_ip_networks = set(ipaddress.ip_network(prefix) for prefix in sa_prefixes_per_origin)
    # create a list to store the aggregated prefixes
    split_prefixes = set()
    # iterate through the list of SA IP networks
    for prefix in sa_ip_networks:
        # iterate through the set of all IP networks to find which SA prefixes can be aggregated by at least one of all IP networks
        broken = 0
        for other_prefix in all_ip_networks:
            if other_prefix.version == prefix.version and other_prefix != prefix and other_prefix.subnet_of(prefix):
                # other_prefix is aggregated by prefix that means that the more specific prefix (other_prefix) 
                # is announced through a customer path, but there is a peer path for the original less specific prefix (prefix), 
                # for fault tolerance reasons. Hence, 'prefix' is a split prefix.
                broken = 1
                break
        if broken: 
            split_prefixes.add(prefix)
    # return the split sa prefixes
    return split_prefixes

def read_anycast_prefixes(url1, url2):
    # open the file in read mode
    with open(url1, 'r') as f1, open(url2, 'r') as f2:
        # read the contents of the file into a list of strings
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # strip any trailing newline characters from each line
    lines1 = [line.strip() for line in lines1]
    lines2 = [line.strip() for line in lines2]

    return lines1 + lines2

# Reads content from a json file
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# Writes content to a json file
def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)


def read_sa_prefixes(collection_year, peer):
    sa_prefixes = read_json(
        'sa_prefixes/' + collection_year + '/' + peer + '_sa_prefixes.json')

    as_paths_per_origin = sa_prefixes['as_path_per_origin']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    return as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin

def flatten_list(list):
    return [val for sublist in list for val in sublist]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Enter a year in range 2003-2023:')
        collection_year = input()
    else:
        collection_year = sys.argv[1]
    while int(collection_year) > 2023 and int(collection_year) < 2003:
        print('Enter a valid year (in the range 2003-2023):')
        collection_year = input()

    peers = ["3292", "3257", "3549", "5511", "7018"]
    peers = ["3292"]
    
    all_peers = [x.split('sa_prefixes/' + collection_year + '/')[1].split('_')[0]
                 for x in glob.glob('sa_prefixes/' + collection_year + '/*.json')]
    all_peers = list(set(all_peers).difference(set(peers)))
    all_observed_prefixes = set()
    for all_peer in all_peers:
        as_paths, prefixes, sa_customer_prefixes = read_sa_prefixes(
            collection_year, all_peer)
        all_observed_prefixes.update(flatten_list([prefixes[key] for key in peers if key in prefixes]))
    all_observed_prefixes = list(all_observed_prefixes)
    as_paths_dict = dict()
    prefixes_dict = dict()
    sa_prefixes_dict = dict()
    anycast_prefixes = read_anycast_prefixes('causes/anycast_prefixes/anycatch-v4-prefixes.txt', 'causes/anycast_prefixes/anycatch-v6-prefixes.txt')
    for peer in peers:
        print(peer)
        as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin = read_sa_prefixes(
            collection_year, peer)
        as_paths_dict[peer] = as_paths_per_origin
        prefixes_dict[peer] = prefixes_per_origin
        sa_prefixes_dict[peer] = sa_customer_prefixes_per_origin

        total_average_of_split_sa_prefixes_per_origin = 0
        total_average_of_aggregatable_sa_prefixes_per_origin = 0
        total_sa_prefixes_per_origin = 0

        num_of_anycasted_sa_prefixes = 0
        split_sa_prefixes = set()
        for idx, origin in enumerate(sa_prefixes_dict[peer]):
            all_prefixes_per_origin = prefixes_dict[peer][origin]
            sa_prefixes_per_origin = sa_prefixes_dict[peer][origin]
            all_prefixes_difference_sa_prefixes_per_origin = list(set(all_prefixes_per_origin).difference(set(sa_prefixes_per_origin)))
            # print(len(all_observed_prefixes))
            # print(len(all_prefixes_difference_sa_prefixes_per_origin))
            
            split_prefixes = find_split_sa_prefixes(
                all_prefixes_difference_sa_prefixes_per_origin, sa_prefixes_per_origin)
            
            aggregatable_prefixes = find_aggregatable_sa_prefixes(
                all_observed_prefixes, sa_prefixes_per_origin)
            total_average_of_split_sa_prefixes_per_origin += len(split_prefixes)/len(sa_prefixes_per_origin)
            total_average_of_aggregatable_sa_prefixes_per_origin += len(aggregatable_prefixes)/len(sa_prefixes_per_origin)
            for prefix in sa_prefixes_per_origin:
                if prefix in anycast_prefixes:
                    num_of_anycasted_sa_prefixes += 1
                total_sa_prefixes_per_origin += 1

        print(total_average_of_split_sa_prefixes_per_origin/len(sa_prefixes_dict[peer].keys()))
        print(total_average_of_aggregatable_sa_prefixes_per_origin/len(sa_prefixes_dict[peer].keys()))
        print(num_of_anycasted_sa_prefixes/total_sa_prefixes_per_origin)




