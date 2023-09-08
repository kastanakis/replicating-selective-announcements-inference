# 20 Years of Inferring Inter-domain Routing Policies
---

## Motivation
In 2003, Wang and Gao presented an algorithm to infer and characterize routing policies as this knowledge could be valuable in predicting and debugging routing paths. They used their algorithm to measure the phenomenon of selectively announced prefixes, in which, ASes would announce their prefixes to specific providers to manipulate incoming traffic. Since 2003, the Internet has evolved from a hierarchical graph, to a flat and dense structure. Despite 20 years of research since that seminal work, the impact of these topological changes on routing policies is still unclear. In this paper we conduct a replicability study of the Wang and Gao paper, to shed light on the evolution and the current state of selectively announced prefixes. We show that selective announcements are persistent, not only across time, but also across networks. Moreover, we observe that neighbors of different AS relationships may be assigned with the same local preference values, and path selection is not as heavily dependent on AS relationships as it used to be. Our results highlight the need for BGP policy inference to be conducted as a high-periodicity process to account for the dynamic nature of AS connectivity and the derived policies.

## Overview
Our methodology consists of the data collection phase and 2 research experiments. 

As in the original Wang and Gao paper, our study of routing policies relies on AS relationship inference. We use the current state-of-the-art AS relationships, made available by CAIDA. For our analysis, we also use data from the RouteViews and RIPE RIS projects through the BGPStream API. Both projects collect routing data from various vantage points across the Internet (i.e., route collectors) and are widely used by network operators and researchers to monitor Internet routing paths and dynamics, and analyze routing policies. Moreover, we leverage data from Looking Glass (LG) servers to study import policies in Section 5. LG servers are interfaces to network devices that provide access to real-time routing information. They can be queried through web-based, telnet or ssh interfaces that allow users to query BGP routing tables or measure traceroute paths from the perspective of the LG server’s location.

In the first research experiment, we observe the Import Routing Policies of different Autonomous Systems (ASes) and study the degree of consistency between the actual routing policies and the inferred AS relationships. Additionally, we study whether the configuration of Import Policies happens based on prefix or next-hop. Finally, since our work relies on inferred AS relationships, we study the potential error introduced by the inferred AS relationships, by comparing the inferred AS relationships against BGP community values. The results of this experiment are in Section 5 in the paper.

In the second research experiment, we infer the Export Routing Policies of different ASes from the point of view of their customers (Section 6 in the paper).

## Data Collection
To collect public routing data for this analysis, head to the **data_collection/** folder and run the respective _route_collection script (i.e., hourly, daily, monthly, yearly). E.g.,

```python3 daily_route_collection.py 22```

would collect the routing tables of the designated vantage points on the 22nd of January, 2023. By running: 

```python3 monthly_route_collection.py 05```

one can download the respective routing tables on the 1st of May (5), 2022.

## Experiment 1: What is the local preference setting among provider, customer and peer routes? 


## Experiment 2: Do customers advertise their prefixes selectively to their providers? 
To extract the SA prefixes from the collected routing tables, run the following script:

```python3 collect_sa_prefixes_for_2003_2023.py 2017```

To study the prevalence ofSA prefixes across different networks, run the following script:

```python3 study_prevalence_of_sa_prefixes_for_2003_2023.py 2017```

To study the persistence of SA prefixes over different years, run the following script:

```python3 study_persistence_of_sa_prefixes_for_2003_2023.py 2017```

To verify the inference of SA prefixes, run the following script:

```python3 verify_sa_prefixes_for_2003_2023.py 2017```

To study the causes of SA prefixes, run the following script:

```python3 study_causes_of_sa_prefixes.py 2017```


 
