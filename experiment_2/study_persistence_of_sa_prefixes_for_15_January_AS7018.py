import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

def study_from_provider_pov(hour):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/2023_15_January_AS7018/' + hour + '_sa_prefixes.json')

    hour = sa_prefixes['hour']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    sa_peer_prefixes_per_origin = sa_prefixes['sa_peer_prefixes_per_origin']

    def flatten_list(list):
        return [val for sublist in list for val in sublist]
    print(hour)
    percentage_of_sa_customer_prefixes = [len(flatten_list(
        sa_customer_prefixes_per_origin.values())) , len(flatten_list(prefixes_per_origin.values()))]
    percentage_of_sa_customer_origins = [len(
        sa_customer_prefixes_per_origin.keys()) , len(prefixes_per_origin.keys())]
    percentage_of_sa_peer_origins = [len(
        sa_peer_prefixes_per_origin.keys()) , len(prefixes_per_origin.keys())]
    return percentage_of_sa_customer_prefixes, percentage_of_sa_customer_origins, percentage_of_sa_peer_origins, sa_prefixes



if __name__ == '__main__':
    sa_origin_announcement_ratio_per_hour = dict()
    sa_prefix_announcement_ratio_per_hour = dict()
    routing_table_metadata_dict = dict()
    for hour in [0, 8, 16]:
        to_write = dict()
        if hour < 9:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        sa_customer_prefixes_ratio, sa_customer_origins_ratio, sa_peer_ratio, routing_table_metadata = study_from_provider_pov(
            hour)
        sa_origin_announcement_ratio_per_hour[hour] = sa_customer_origins_ratio
        sa_prefix_announcement_ratio_per_hour[hour] = sa_customer_prefixes_ratio
        routing_table_metadata_dict[hour] = routing_table_metadata

    write_json('persistence/per_hour_AS7018/hourly_SA_origins.json',
               sa_origin_announcement_ratio_per_hour)
    write_json('persistence/per_hour_AS7018/hourly_SA_prefixes.json',
               sa_prefix_announcement_ratio_per_hour)
    
    # Extract the first and second values from the data
    values1 = [v[0] for k, v in sa_prefix_announcement_ratio_per_hour.items()]
    values2 = [v[1] for k, v in sa_prefix_announcement_ratio_per_hour.items()]
    average_values = [values1[index]/item for index, item in enumerate(values2)]
    print(average_values)
    # Create a list of hours as x-axis labels
    hours = [str(k) + ":00" for k, v in sa_prefix_announcement_ratio_per_hour.items()]

    FONT_SIZE = 13
    plt.rcParams.update({'font.size': FONT_SIZE})

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the width of each bar
    width = 0.35

    # Plot the second set of bars on top of the first set
    ax.bar(hours, values2, width,
           label='All Prefixes', edgecolor='black', color='white')
    
    # Plot the first set of bars
    ax.bar(hours, values1, width, label='SA Prefixes',
           edgecolor='black', color='black')


    # Add labels and title
    ax.set_xlabel('Hours (during January 15, 2023)')
    ax.set_ylabel('Number of Prefixes')
    plt.tight_layout()
    plt.grid()
    # plt.setp(ax.get_xticklabels()[1::2], visible=False)

    # Add legend
    ax.legend()
    plt.savefig("persistence/per_hour_AS7018/sa_prefixes_AS7018_hourly_barplot.png")


    # Extract the first and second values from the data
    values1 = [v[0] for k, v in sa_origin_announcement_ratio_per_hour.items()]
    values2 = [v[1] for k, v in sa_origin_announcement_ratio_per_hour.items()]

    # Create a list of hours as x-axis labels
    hours = [str(k) + ":00" for k, v in sa_origin_announcement_ratio_per_hour.items()]

    FONT_SIZE = 13

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the width of each bar
    width = 0.35

    # Plot the second set of bars on top of the first set
    ax.bar(hours, values2, width,
           label='All Origins', edgecolor='black', color='white')
    
    # Plot the first set of bars
    ax.bar(hours, values1, width, label='SA Origins',
           color='black', edgecolor='black')


    # Add labels and title
    plt.rcParams.update({'font.size': FONT_SIZE})
    ax.set_xlabel('Hours (during January 15, 2023)')
    ax.set_ylabel('Number of Origins')
    plt.tight_layout()
    plt.grid()
    # plt.setp(ax.get_xticklabels()[1::2], visible=False)
    # Add legend
    ax.legend()
    plt.savefig(
        "persistence/per_hour_AS7018/sa_origins_AS7018_hourly_barplot.png")
