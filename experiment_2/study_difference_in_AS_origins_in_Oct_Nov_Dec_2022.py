import statsmodels.api as sm
import sys
import json
from infer_sa_prefixes import *
from pprint import pprint as pprint
import matplotlib.pyplot as plt
import numpy as np

# Reads content from a json file
def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)

# Writes content to a json file
def write_json(jsonfilename, content):
    with open(jsonfilename, 'w+') as fp:
        json.dump(content, fp, indent=4)

def read_sa_prefixes(month, peer):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/2022_AS7018/' + month + '_sa_prefixes.json')

    as_paths_per_origin = sa_prefixes['as_path_per_origin']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    return as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin


if __name__ == '__main__':
    as_paths_dict = dict()
    prefixes_dict = dict()
    sa_prefixes_dict = dict()
    counter_dict = dict()
    for month in range(0, 12):
        to_write = dict()
        if month < 9:
            month += 1
            month = '0' + str(month)
        else:
            month += 1
            month = str(month)

        print(month)
        as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin = read_sa_prefixes(
            month, '7018')
        as_paths_dict[month] = as_paths_per_origin
        prefixes_dict[month] = prefixes_per_origin
        sa_prefixes_dict[month] = sa_customer_prefixes_per_origin
    
    def flatten_list(list):
        return [val for sublist in list for val in sublist]
    all_prefixes_intersection = set()
    for month in range(0, 12):
        if month < 9:
            month += 1
            month = '0' + str(month)
        else:
            month += 1
            month = str(month)
        if month == '01':
            all_prefixes_intersection = set(
                flatten_list(prefixes_dict[month].values()))
        else:
            all_prefixes_intersection.intersection(
                set(flatten_list(prefixes_dict[month].values())))
      
    oct_set = set(flatten_list(sa_prefixes_dict['10'].values())).intersection(all_prefixes_intersection)
    nov_set = set(flatten_list(sa_prefixes_dict['11'].values())).intersection(all_prefixes_intersection)
    dec_set = set(flatten_list(sa_prefixes_dict['12'].values())).intersection(
        all_prefixes_intersection)
    
    print(len(list(all_prefixes_intersection)))
    print(len(list(oct_set)))
    print(len(list(nov_set)))
    print(len(list(dec_set)))
    print(len(list(oct_set.intersection(nov_set))))
    print(len(list(nov_set.intersection(dec_set))))
    print(len(list(oct_set.intersection(dec_set))))
    print(len(list(oct_set.intersection(dec_set).intersection(nov_set))))
    print(len(list(oct_set.intersection(dec_set).difference(nov_set))))
    print(len(list(oct_set.intersection(nov_set).difference((nov_set.intersection(dec_set))))))
    
