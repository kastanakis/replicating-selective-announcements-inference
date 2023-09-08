import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

def read_sa_prefixes(day, peer):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/2023_January_AS7018/' + day + '_sa_prefixes.json')

    as_paths_per_origin = sa_prefixes['as_path_per_origin']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    return as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin


if __name__ == '__main__':
    as_paths_dict = dict()
    prefixes_dict = dict()
    sa_prefixes_dict = dict()
    counter_dict = dict()
    for day in range(0, 31):
        to_write = dict()
        if day < 9:
            day += 1
            day = '0' + str(day)
        else:
            day += 1
            day = str(day)

        print(day)
        as_paths_per_origin, prefixes_per_origin, sa_customer_prefixes_per_origin = read_sa_prefixes(
            day, '7018')
        as_paths_dict[day] = as_paths_per_origin
        prefixes_dict[day] = prefixes_per_origin
        sa_prefixes_dict[day] = sa_customer_prefixes_per_origin

        for origin in sa_prefixes_dict[day]:
            for prefix in sa_prefixes_dict[day][origin]:
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
    plt.xlabel('Days')
    plt.ylabel('CDF of SA prefixes\' uptime')
    plt.grid()
    plt.tight_layout()

    # Save the plot
    write_json('uptime/uptime_sa_prefixes_AS7018_daily_ecdf.json', counter_dict)
    plt.savefig("uptime/uptime_sa_prefixes_AS7018_daily_ecdf.png")
