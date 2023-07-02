import sys
import csv
import networkx as nx
from collections import defaultdict
from pprint import pprint as pprint
import glob

# Reads the topology dataset in a NetworkX graph
def get_AS_relationships_graph(as2rel_mapping):
    G = nx.DiGraph()
    with open(as2rel_mapping, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')
        for row in csvreader:
            if row[0][0] != '#':  # ignore lines starting with "#"
                as1 = row[0]
                as2 = row[1]
                rel = int(row[2])
                if rel == -1:
                    G.add_edge(as1, as2)
                elif rel == 0:
                    G.add_edge(as1, as2)
                    G.add_edge(as2, as1)
    return G

# Algorithm for inferring export policy: Phases 1 and 2
def customer_cone_dfs(G, u):
    # Phase 1
    visited = set()
    customer_cone = set()
    S = [u]
    # Phase 2
    while S:
        node = S.pop()
        if node not in visited:
            visited.add(node)
            if node not in G:
                return customer_cone
            for neighbor in G.neighbors(node):
                # If node is not in neighbor's neighbors, then node is a provider of neighbor, else peer/customer
                # We only want to traverse customer paths in this phase, not peer paths.
                if node not in G.neighbors(neighbor):
                    # If is a direct/indirect customer of u, add it into customer cone
                    if neighbor not in visited:
                        customer_cone.add(neighbor)
                        S.append(neighbor)
    return customer_cone

# Algorithm for inferring export policy: Phase 3
def is_provider(G, w, u):
    if u not in G or w not in G: return False
    return w in G.neighbors(u) and u not in G.neighbors(w)

# Algorithm for inferring export policy: Phase 3
def is_peer(G, w, u):
    if u not in G or w not in G: return False
    return w in G.neighbors(u) and u in G.neighbors(w)

# Wrapper function for inferring export policy of direct/indirect customers
def is_selective_announcement_customer(AS_relationships_graph, route, customer_cone_graph):
    vantage_point = route[7]
    prefix = route[9]
    origin_as = route[11].split(" ")[-1]
    next_hop_as = route[11].split(" ")[1]
    # Phases 1 and 2
    if origin_as in customer_cone_graph:
        # Phase 3
        if not is_provider(AS_relationships_graph, next_hop_as, vantage_point):
            return True
        return False
    return False


# Wrapper function for inferring export policy of direct/indirect customers
def is_selective_announcement_peer(AS_relationships_graph, route):
    vantage_point = route[7]
    prefix = route[9]
    origin_as = route[11].split(" ")[-1]
    next_hop_as = route[11].split(" ")[1]
    # Phases 1 and 2
    if is_peer(AS_relationships_graph, origin_as, vantage_point):
        # Phase 3
        if is_provider(AS_relationships_graph, vantage_point, next_hop_as):
            return True
        return False
    return False
