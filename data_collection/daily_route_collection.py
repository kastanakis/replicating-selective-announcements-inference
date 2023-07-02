import sys
sys.path.append('imc-repro23-inferring/data_collection/')
from __dc_lib__ import *

def main(date=""):
    ''' 
    BGP Elem Format: check https://bgpstream.caida.org/docs/tools/bgpreader#elem.
    <dump-type>|<elem-type>|<record-ts>|<project>|<collector>|<router-name>|<router-ip>| \
    <peer-ASn>|<peer-IP>|<prefix>|<next-hop-IP>|<AS-path>|<communities>|<old-state>|<new-state>
    '''

    from_time = date + " 00:00:00"
    until_time = date + " 00:00:00 UTC"
    print((from_time, until_time))

    # Check the full list of providers here: https://bgpstream.caida.org/data#!ris and here: https://bgpstream.caida.org/data#!routeviews
    stream = pybgpstream.BGPStream(
        from_time=from_time, until_time=until_time,
        # this implies that we are using all possible route collectors
        projects=['ris', 'routeviews'],
        record_type="ribs",
        filter="peer 7018"
    )
    routing_tables_location = 'output/routing_tables/2023_January_AS7018/'
    day = date.split('-')[2]
    write_from_stream_to_file(routing_tables_location, stream, day)


if __name__ == "__main__":
    # Collect rib dumps from 1st of April of a given year from all route collectors (RIPEris and RouteViews)
    if len(sys.argv) < 2:
        print('Enter a day in range 1-31:')
        day_of_collection = input()
    else:
        day_of_collection = sys.argv[1]
    while int(day_of_collection) > 31 or int(day_of_collection) < 1:
        print('Enter a valid day (in the range 1-31):')
        day_of_collection = input()
    if int(day_of_collection) < 10:
        day_of_collection = '0' + str(day_of_collection)
    main("2023-01-" + day_of_collection)
