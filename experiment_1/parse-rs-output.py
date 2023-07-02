import re
import os
import bz2
import gzip
from collections import defaultdict


# Works for 62887, 2495, 6730
router_type = dict()
router_type["juniper"] = ["2495", "62887"]
router_type["cisco"] = ["6730"]
target_autsys = "6730"

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
localpref_neighbors = defaultdict(set)
relationship_localpref = defaultdict(lambda: defaultdict(int))
aspath_pattern = "AS path: "
pattern = re.compile("([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}/[0-9]{1,2})")
rs_dumps = os.listdir(target_directory)
for rs_dump in rs_dumps:
    if not rs_dump.startswith(target_autsys): continue
    rs_dump_filepath = os.path.join(target_directory, rs_dump)
    print(rs_dump_filepath)
    with gzip.open(rs_dump_filepath, "rt") as fin:
        ip_prefix = None
        autsys_path = None
        local_pref = None
        for line in fin:
            pattern_match = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}", line)
            if len(pattern_match) > 0:
                ip_prefix = pattern_match[0]
            if target_autsys in router_type["juniper"]:
                if "localpref" in line and "from" in line:
                    line_fields = re.split(",| ", line)
                    local_pref_index = line_fields.index("localpref") + 1
                    local_pref = int(line_fields[local_pref_index])

                if aspath_pattern in line:
                    line = line.strip()
                    autsys_path_index = line.index(aspath_pattern) + len(aspath_pattern)
                    line_fields = re.split(",| +|:", line[autsys_path_index:])
                    try:
                        if "validation-state" in line_fields:
                            origin_index = line_fields.index("validation-state") - 2
                        elif "I" in line_fields:
                            origin_index = line_fields.index("I") - 2
                        else:
                            continue
                        autsys_path = line_fields[0:origin_index]
                        neighbor = autsys_path[0]
                        localpref_neighbors[local_pref].add(neighbor)
                        if neighbor in neighbor_relationships:
                            relationship = neighbor_relationships[neighbor]
                        else:
                            relationship = "unknown"
                        relationship_localpref[relationship][local_pref] += 1
                    except ValueError as e:
                        continue
                    except IndexError as e:
                        continue
            elif target_autsys in router_type["cisco"] and ip_prefix is not None:
                lf = line.strip().split()
                try:
                    if len(lf) > 0 and lf[-1].lower() == "i" and lf[-2] != "0":
                        reverse_attributes = lf[::-1]
                        for index, field in enumerate(reverse_attributes):
                            if field == "0":
                                local_pref = reverse_attributes[index + 1]

                                neighbor = reverse_attributes[index - 1]
                                localpref_neighbors[local_pref].add(neighbor)
                                if neighbor in neighbor_relationships:
                                    relationship = neighbor_relationships[neighbor]
                                else:
                                    relationship = "unknown"
                                relationship_localpref[relationship][local_pref] += 1
                                break
                except IndexError:
                    raise


for local_pref, neighbors in localpref_neighbors.items():
    print(local_pref, neighbors)

for relationship in relationship_localpref:
    for localpref, values in relationship_localpref[relationship].items():
        print(relationship, localpref, values)
