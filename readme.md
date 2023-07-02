# Revisiting the problem of inferring and characterizing Internet routing policies 20 years later
---

## Motivation
We replicate the *"Wang, F., & Gao, L. (2003, October). On inferring and characterizing Internet routing policies. In Proceedings of the 3rd ACM SIGCOMM conference on Internet measurement (pp. 15-26)"* for the ACM Internet Measurement Conference 2023 Replicability Track.

## Data source collection 
- The authors in IMC'03 use BGP tables from public route collectors (see https://bgpstream.caida.org/) and public route servers (see https://www.routeservers.org/). 

## Experiment 1: What is the local preference setting among provider, customer and peer routes? 
- For each route in the routing tables:  
  - They collect the local preference value and the first-hop AS-relationship 
    - To infer the AS-relationship between the source AS and the next-hop AS they use AS-relationships data, similar to CAIDA’s AS-relationships. 
    - They validate AS-relationships through BGP community clustering (see Appendix of IMC’03) 
  - They question if the local preference values follow a common pattern per business relationship?  
    - Yes they do, mostly typical local preference. 
  - They question if local preference values are set based on next-hop? 
    - They tested ATT routing tables from 30 backbone routers.  
    - ASes tend to assign localpref based on next-hop 

## Experiment 2: Do customers advertise their prefixes selectively to their providers? 
The algorithm for inferring export policies is the following: 
- For every neighbor N of an AS P: 
  - If N is a direct/indirect customer of P and  
  - If N originates at least one prefix for which there is not a single customer route from P then N is candidate for selective announcement. 
  - To verify a selective announcement, the authors try to find active customer paths towards the selective announced prefix by searching all paths in BGP routing tables.
 - What is the prevalence and persistence of SA prefixes? (i.e., over multiple ASes and over time) 
 

 

## Experiment 3: What are the causes of selective announced prefixes? 
- Is it prefix splitting? 
- Is it prefix aggregating? 
- Is there an intermediate customer that receive these prefixes but do not export them? 
- Is it selective announcing? 
  - They studied AS1 (since it had 32% of SA prefixes) and its direct customers, to tell if there is a direct elective announcement: yes there is, 79% of customers do selective advertising. 

 
