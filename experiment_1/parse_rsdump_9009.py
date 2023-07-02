import re
import os
import bz2
import gzip
from collections import defaultdict

target_autsys = '9009'

##patterns
pattern_num = '^[0-9]+$'
pattern_nexthop='[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'
pattern_prefix='[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}'

pattern_start='^\*>i[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2}'
error_item = ('nan', 'nan', -1, -1)



def ck_type(vin_item, vin_index):
    ''' Test the token types. Returns false/true. Input: token, type '''
    if vin_index == 0 and not re.match(pattern_prefix, vin_item):
        return 0
    if vin_index == 1 and not re.match(pattern_nexthop, vin_item):
        return 0
    if vin_index == 3 and not re.match(pattern_num, vin_item):
        return 0
    if vin_index == 5 and not re.match(pattern_num, vin_item):
        return 0
    return 1

def parse_line(vin_line):
    ''' parse one line from RS dump. Returns: prefix, nexthop, localpref, neighbor. Input: line'''
    ln = [item for item in line.strip().split(' ') if item != '']
    llprefix = ln[0][3:]
    llnexthop = ln[1]
    llmetric = ln[2]
    lllocal_pref = ln[3]
    llweight = ln[4]
    llneighbor = ln[5:-1][0]
    
    ##test the extracted items
    if not ck_type(llprefix, 0) or not ck_type(llnexthop, 1) or not ck_type(lllocal_pref, 3) or not ck_type(llneighbor,5):
        print ('Error: Found token that fails check')
        return error_item
    return (llprefix, llnexthop, int(lllocal_pref), llneighbor)

neighbor_relationships = defaultdict(str)
asrels_filepath = "data/20230301.as-rel.txt.bz2"
with bz2.open(asrels_filepath, "rt") as fin:
    for line in fin:
        if not line.startswith("#"):
            lf = line.strip().split("|")
            if lf[0] == target_autsys:
                if lf[2] == "0":
                    neighbor_relationships[lf[1]] = "peer"
                elif lf[2] == "-1":
                    neighbor_relationships[lf[1]] = "customer"
            if lf[1] == target_autsys:
                if lf[2] == "0":
                    neighbor_relationships[lf[0]] = "peer"
                elif lf[2] == "-1":
                    neighbor_relationships[lf[0]] = "provider"

target_directory = "./RS dumps"
rs_dumps = os.listdir(target_directory)

localpref_neighbors = defaultdict(set)
relationship_localpref = defaultdict(lambda: defaultdict(int))
for rs_dump in rs_dumps:
    if not rs_dump.startswith(target_autsys): continue
    rs_dump_filepath = os.path.join(target_directory, rs_dump)
    print('Parse:' + rs_dump_filepath)
    with open(rs_dump_filepath, "r") as fin:
        ip_prefix = None
        autsys_path = None
        local_pref = None
        for line in fin:
            #if not line.startswith(pattern_start): continue
            if not re.match(pattern_start, line.strip()): continue
            #line :    Network          Next Hop            Metric LocPrf   Weight Path
            ##line: *>i0.0.0.0          193.27.64.1              0    100      0 i
            prefix, nexthop, local_pref, neighbor = parse_line(line.strip())
            localpref_neighbors[local_pref].add(neighbor)
            if neighbor in neighbor_relationships:
                relationship = neighbor_relationships[neighbor]
            else:
                relationship = "unknown"
            relationship_localpref[relationship][local_pref] += 1    

for local_pref, neighbors in localpref_neighbors.items():
    print(local_pref, neighbors)

for relationship in relationship_localpref:
    for localpref, values in relationship_localpref[relationship].items():
        print(relationship, localpref, values)

            