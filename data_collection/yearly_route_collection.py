import sys
sys.path.append('imc-repro23-inferring/data_collection/')
from __dc_lib__ import *

# Writes under the selective collection year folder, the routing table of the respective peer ASn
def write_from_stream_to_file(routing_tables_location, stream):
    # We consider only the routing tables of the following ASns
    vantage_points = ["553", "852", "1280", "1916", "2500", "3257", "3292", "3303", "3549", "3582",
                      "3741", "4589", "4706", "4826", "5413", "5453", "5511", "5713", "6667", "6730",
                      "6939", "7012", "7018", "7474", "7922", "8301", "8881", "9009", "11260", "11404",
                      "12276", "12389", "13645", "14609", "15290", "15763", "17435", "18881",
                      "19653", "20751", "22548", "24218", "25376", "26689", "27552", "31027", "31672",
                      "36086", "37100", "37255", "37271", "37474", "37578", "45186", "45494", "49983",
                      "52965", "53062", "53164", "56911", "59105", "62887", "63221", "133072", "210083"]
    # We populate two pytricia trees to keep track of the bogus prefixes
    filename1 = 'input/fullbogons-ipv4.txt'
    filename2 = 'input/fullbogons-ipv6.txt'
    bogons_pyt_v4, bogons_pyt_v6 = create_bogons_trees(filename1, filename2)
    # We filter out element with cycles, invalid prefixes, or non vantage point ASn
    for elem in stream:
        row = str(elem).split('|')
        # Discard {ASn} occurences
        res = [i for i in row if '{' in i]
        if res:
            continue
        record_type = row[0]
        type = row[1]
        peer_asn = row[7]
        prefix = row[9]
        as_path = row[11]

        # if record_type == "update" and type == "A":
        if record_type == "rib" and type == "R":
            # Only consider routes for which we have a route-server to use
            if peer_asn not in vantage_points:
                continue
            if is_valid(prefix, bogons_pyt_v4, bogons_pyt_v6):
                # Get the list of ASes in the AS path
                as_path_list = as_path.split(" ")
                # Remove path prepending
                as_path_filtered = remove_prepending(as_path_list)
                # Discard paths with cycles and with less than 2 ASes
                if not has_cycle(as_path_filtered) and len(as_path_filtered) > 1:
                    # Write the original entry into the filtered csv
                    with open(routing_tables_location + peer_asn + '_routing_table.csv', 'a+') as output_csv_file:
                        csv_writer = csv.writer(output_csv_file, delimiter='|')
                        csv_writer.writerow(row)


def main(date=""):
    ''' 
    BGP Elem Format: check https://bgpstream.caida.org/docs/tools/bgpreader#elem.
    <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<router-name>|<router-ip>| \
    <peer-ASn>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<communities>|<old-state>|<new-state>
    '''

    from_time = date + " 00:00:00"
    until_time = date + " 00:15:00 UTC"
    print((from_time, until_time))

    # Check the full list of providers here: https://bgpstream.caida.org/data#!ris and here: https://bgpstream.caida.org/data#!routeviews
    stream = pybgpstream.BGPStream(
        from_time=from_time, until_time=until_time,
        # this implies that we are using all possible route collectors
        projects=['ris', 'routeviews'],
        record_type="ribs"
    )
    routing_tables_location = 'output/routing_tables/' + date.split('-')[0] + '/'

    write_from_stream_to_file(routing_tables_location, stream)


if __name__ == "__main__":
    # Collect rib dumps from 1st of April of a given year from all route collectors (RIPEris and RouteViews)
    if len(sys.argv) < 2:
        print('Enter a year in range 2003-2023:')
        year_of_collection = input()
    else:
        year_of_collection = sys.argv[1]
    while int(year_of_collection) > 2023 or int(year_of_collection) < 2003:
        print('Enter a valid year (in the range 2003-2023):')
        year_of_collection = input()
    main(date=year_of_collection + "-04-01")
