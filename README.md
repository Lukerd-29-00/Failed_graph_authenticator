# Graph Isomorphsim ZKP: Flawed client
This is a graph-isomorphism based zero-knowledge proof scheme that was implemented incorrectly. The flawed protocol is below.

## Protocol
Alice requests a graph that is isomorphic to G0, along with a mapping from that graph to G0. Automorphisms are rejected. She proves her knowledge of the secret by mapping this graph to G1. This deviates from the secure protocol, where the server would ask alice for a graph, then randomly ask her to map it to G0 or to G1.

## Challenge files
graph.py, alice.py, gen_key.py (optional), public_key.json (optional). This is technically solvable with only alice.py. alice.py and server.py should be run as services.

## Solution
It is trivial for someone posing as the server to extract alice's secret. All they need to do is follow the protocol, then compute -i + m where m is alice's response and i is the mapping from the graph they generated to G0. Addition represents the composition of the two transformations on the graph. Note that the group of isomorphisms is non-abelian, meaning that m - i **will not work**.

## A note on documentation
The graph library is not well documented, but for this problem, it really doesn't need to be. A quick glance at alice.py and the Isomorphism class should be good enough.

## Graph encoding
The graphs only support vertices from 0 to the max number - 1. They are stored internally as an adjacency matrix with the redundant half removed (because the graphs are undirected). This is serialized into booleans, which are converted into an integer via bitwise OR so that each edge is stored in only one bit.