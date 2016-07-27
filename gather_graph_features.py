#!/usr/bin/python
import glob
import os
import networkx as nx
from graph_tool.all import *

all_graphs = {}
files = filter(os.path.isfile, glob.glob("*"))
for f in files:
    if not f.endswith('.gt'): continue
    code = f.split('/')[-1].split('.')[0]
    print code
    gr = load_graph(f, fmt="gt")
    remove_parallel_edges(gr)
    remove_self_loops(gr)
    all_graphs[code] = gr
    
all_graphs_networkx = {}
for code, gr in all_graphs.iteritems():
    remove_parallel_edges(gr)
    remove_self_loops(gr)
    G = nx.Graph()
    for edge in gr.edges():
        src = gr.vp.asn[edge.source()]
        dst = gr.vp.asn[edge.target()]
        G.add_edge(src, dst)
    if not nx.is_connected(G):
        G = sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    all_graphs_networkx[code] = G
