import pandas as pd

# calculate the number of ASes and links by year
years = [1998] + list(range(2003, 2024))
ases = []
links = []
peer_links = []
peer_ratio = []
for year in years:
    AS_relationships_url = '../__CAIDA_AS-graph__/' + \
        str(year) + '0401.as-rel.txt'
    data = pd.read_csv(AS_relationships_url, comment='#', delimiter='|',
                       header=None, names=["AS1", "AS2", "relationship", "method"])

    # calculate the number of unique ASes
    num_ases = len(pd.concat([data["AS1"], data["AS2"]]).unique())
    ases.append(num_ases)

    # calculate the total number of links
    num_links = len(data)
    links.append(num_links)

    # calculate the number of peer links
    num_peer_links = len(data[data["relationship"] == 0])
    peer_links.append(num_peer_links)

    # calculate the ratio of peer links to total links
    peer_link_ratio = num_peer_links / num_links
    peer_ratio.append(int(peer_link_ratio * 100))

# create a dataframe to hold the results
df = pd.DataFrame({
    "Year": years,
    "ASes": ases,
    "Links": links,
    "Peer Links": peer_links,
    "% of Peer Links": peer_ratio
})

# print the dataframe
print(df)
#     Year   ASes   Links  Peer Links  % of Peer Links
# 0   2003  15164   35440        7084               19
# 1   2004  17303   43804       11185               25
# 2   2005  19552   50111       13379               26
# 3   2006  22125   58516       16387               28
# 4   2007  25133   67886       19641               28
# 5   2008  28153   79590       25272               31
# 6   2009  31596   84557       24159               28
# 7   2010  34287   95531       30799               32
# 8   2011  37571  111271       39512               35
# 9   2012  40989  126082       48003               38
# 10  2013  44064  143894       58366               40
# 11  2014  45636  167005       75930               45
# 12  2015  50315  191634       91635               47
# 13  2016  53792  219855      116209               52
# 14  2017  57256  246143      131639               53
# 15  2018  60874  300634      178608               59
# 16  2019  64550  330558      201827               61
# 17  2020  68289  369083      233845               63
# 18  2021  71665  364531      217870               59
# 19  2022  73807  418482      270879               64
# 20  2023  75160  494508      341363               69
