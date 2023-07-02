from infer_sa_prefixes import *
import json
from pprint import pprint as pprint
from itertools import groupby
from operator import itemgetter
from pprint import pprint as pprint
import matplotlib.pyplot as plt
import ipaddress

# Reads content from a json file


def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# Writes content to a json file


def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)

# Removes consecutive duplicates in a sequence


def remove_prepending(seq):
    # https://stackoverflow.com/questions/5738901/removing-elements-that-have-consecutive-duplicates
    return list(map(itemgetter(0), groupby(seq)))

# Collects SA prefixes from the respective routing tables


def collect_sa_prefixes(AS_relationships_graph, routing_table, peer):
    as_path_per_origin = defaultdict(list)
    prefixes_per_origin = defaultdict(list)
    sa_customer_prefixes_per_origin = defaultdict(list)
    sa_peer_prefixes_per_origin = defaultdict(list)
    customer_cone_graph = customer_cone_dfs(AS_relationships_graph, peer)
    with open(routing_table) as csv_file:
        total_lines = sum(1 for row in csv_file)
    # print(total_lines)
    count = 0
    with open(routing_table, 'r') as input_csv_file:
        csv_reader = csv.reader(input_csv_file, delimiter='|')
        for route in csv_reader:
            print('Completion percentage {}\r'.format(
                count/total_lines), end='')
            count += 1
            prefix = route[9]
            as_path = route[11].split(" ")
            as_path_without_prepending = remove_prepending(as_path)
            origin_as = as_path[-1]
            if as_path_without_prepending not in as_path_per_origin[origin_as]:
                as_path_per_origin[origin_as].append(
                    as_path_without_prepending)
            if prefix not in prefixes_per_origin[origin_as]:
                prefixes_per_origin[origin_as].append(prefix)
            if is_selective_announcement_customer(AS_relationships_graph, route, customer_cone_graph):
                if prefix not in sa_customer_prefixes_per_origin[origin_as]:
                    sa_customer_prefixes_per_origin[origin_as].append(prefix)
            if is_selective_announcement_peer(AS_relationships_graph, route):
                if prefix not in sa_peer_prefixes_per_origin[origin_as]:
                    sa_peer_prefixes_per_origin[origin_as].append(prefix)
    return as_path_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin, sa_peer_prefixes_per_origin
