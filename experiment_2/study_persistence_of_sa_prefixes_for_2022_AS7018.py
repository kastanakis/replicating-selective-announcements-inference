import sys
sys.path.append('imc-repro23-inferring/experiment_2/')
from __exp2_lib__ import *

def study_from_provider_pov(month):
    to_write = dict()
    sa_prefixes = read_json(
        'sa_prefixes/2022_AS7018/' + month + '_sa_prefixes.json')

    month = sa_prefixes['month']
    prefixes_per_origin = sa_prefixes['prefixes_per_origin']
    sa_customer_prefixes_per_origin = sa_prefixes['sa_customer_prefixes_per_origin']
    sa_peer_prefixes_per_origin = sa_prefixes['sa_peer_prefixes_per_origin']

    def flatten_list(list):
        return [val for sublist in list for val in sublist]
    print(month)
    percentage_of_sa_customer_prefixes = [len(flatten_list(
        sa_customer_prefixes_per_origin.values())), len(flatten_list(prefixes_per_origin.values()))]
    percentage_of_sa_customer_origins = [len(
        sa_customer_prefixes_per_origin.keys()), len(prefixes_per_origin.keys())]
    percentage_of_sa_peer_origins = [len(
        sa_peer_prefixes_per_origin.keys()), len(prefixes_per_origin.keys())]
    return percentage_of_sa_customer_prefixes, percentage_of_sa_customer_origins, percentage_of_sa_peer_origins, sa_prefixes


if __name__ == '__main__':
    sa_origin_announcement_ratio_per_month = dict()
    sa_prefix_announcement_ratio_per_month = dict()
    routing_table_metadata_dict = dict()
    for month in range(0, 12):
        to_write = dict()
        if month < 9:
            month += 1
            month = '0' + str(month)
        else:
            month += 1
            month = str(month)
        sa_customer_prefixes_ratio, sa_customer_origins_ratio, sa_peer_ratio, routing_table_metadata = study_from_provider_pov(
            month)
        sa_origin_announcement_ratio_per_month[month] = sa_customer_origins_ratio
        sa_prefix_announcement_ratio_per_month[month] = sa_customer_prefixes_ratio
        routing_table_metadata_dict[month] = routing_table_metadata

    write_json('persistence/per_month_AS7018/monthly_SA_origins.json',
               sa_origin_announcement_ratio_per_month)
    write_json('persistence/per_month_AS7018/monthly_SA_prefixes.json',
               sa_prefix_announcement_ratio_per_month)

    # Extract the first and second values from the data
    values1 = [v[0] for k, v in sa_prefix_announcement_ratio_per_month.items()]
    values2 = [v[1] for k, v in sa_prefix_announcement_ratio_per_month.items()]

    # Create a list of months as x-axis labels
    months = [k for k, v in sa_prefix_announcement_ratio_per_month.items()]

    FONT_SIZE = 13
    plt.rcParams.update({'font.size': FONT_SIZE})

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the width of each bar
    width = 0.35

    # Plot the second set of bars on top of the first set
    ax.bar(months, values2, width, label='All Prefixes', edgecolor='black', color='white')
    # Plot the first set of bars
    ax.bar(months, values1, width, label='SA Prefixes',
           edgecolor='black', color='black')

    # Add labels and title
    ax.set_xlabel('Months (in 2022)')
    ax.set_ylabel('Number of Prefixes')
    plt.tight_layout()
    plt.grid()
    # plt.setp(ax.get_xticklabels()[1::2], visible=False)

    # Add legend
    ax.legend()
    plt.savefig(
        "persistence/per_month_AS7018/sa_prefixes_AS7018_monthly_barplot.png")

    # Extract the first and second values from the data
    values1 = [v[0] for k, v in sa_origin_announcement_ratio_per_month.items()]
    values2 = [v[1] for k, v in sa_origin_announcement_ratio_per_month.items()]

    # Create a list of months as x-axis labels
    months = [k for k, v in sa_origin_announcement_ratio_per_month.items()]

    FONT_SIZE = 13

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the width of each bar
    width = 0.35

    # Plot the second set of bars on top of the first set
    ax.bar(months, values2, width,
           label='All Origins', edgecolor='black', color='white')
    
    # Plot the first set of bars
    ax.bar(months, values1, width, label='SA Origins',
           edgecolor='black', color='black')


    # Add labels and title
    plt.rcParams.update({'font.size': FONT_SIZE})
    ax.set_xlabel('Months (in 2022)')
    ax.set_ylabel('Number of Origins')
    plt.tight_layout()
    plt.grid()
    # plt.setp(ax.get_xticklabels()[1::2], visible=False)
    # Add legend
    ax.legend()
    plt.savefig(
        "persistence/per_month_AS7018/sa_origins_AS7018_monthly_barplot.png")
