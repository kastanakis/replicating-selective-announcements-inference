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

        for origin in sa_prefixes_dict[month]:
            for prefix in sa_prefixes_dict[month][origin]:
                if prefix not in counter_dict:
                    counter_dict[prefix] = 1
                else:
                    counter_dict[prefix] += 1
                   
    # Extract the data
    data = list(counter_dict.values())

    # Calculate the ECDF
    ecdf = sm.distributions.ECDF(data)

    # # Evaluate the ECDF at the x values
    plt.step(ecdf.x, ecdf.y, where='post', color='black')
    plt.xlabel('Months')
    plt.ylabel('CDF of SA prefixes\' uptime')
    plt.grid()
    plt.tight_layout()

    # Save the plot
    write_json('uptime/uptime_sa_prefixes_AS7018_monthly_ecdf.json', counter_dict)
    plt.savefig("uptime/uptime_sa_prefixes_AS7018_monthly_ecdf.png")
