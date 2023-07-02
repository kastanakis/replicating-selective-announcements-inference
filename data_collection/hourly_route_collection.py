import sys
sys.path.append('imc-repro23-inferring/data_collection/')
from __dc_lib__ import *

def main(date="", hour=""):
    ''' 
    BGP Elem Format: check https://bgpstream.caida.org/docs/tools/bgpreader#elem.
    <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<router-name>|<router-ip>| \
    <peer-ASn>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<communities>|<old-state>|<new-state>
    '''

    from_time = date + " " + hour + ":00:00"
    until_time = date + " " + hour + ":00:00 UTC"
    print((from_time, until_time))

    # Check the full list of providers here: https://bgpstream.caida.org/data#!ris and here: https://bgpstream.caida.org/data#!routeviews
    stream = pybgpstream.BGPStream(
        from_time=from_time, until_time=until_time,
        # this implies that we are using all possible route collectors
        projects=['ris', 'routeviews'],
        record_type="ribs",
        filter="peer 7018"
    )
    routing_tables_location = 'output/routing_tables/2023_15_January_AS7018/'
    write_from_stream_to_file(routing_tables_location, stream, hour)


if __name__ == "__main__":
    # Collect rib dumps from 1st of April of a given year from all route collectors (RIPEris and RouteViews)
    if len(sys.argv) < 2:
        print('Enter an hour in range 0-22:')
        hour_of_collection = input()
    else:
        hour_of_collection = sys.argv[1]
    while int(hour_of_collection) > 22 or int(hour_of_collection) < 00:
        print('Enter a valid hour (in the range 0-22):')
        hour_of_collection = input()
    if int(hour_of_collection) < 10:
        hour_of_collection = '0' + str(hour_of_collection)
    main("2023-01-15", hour_of_collection)
