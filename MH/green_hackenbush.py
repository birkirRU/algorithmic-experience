import random
import sys
sys.setrecursionlimit(1000000)
timer = 1

def dfs_bridges(node: int,
        parent_eid: int, 
        vis: list[int],
        adj: list[int],
        tin: list[int],
        low: list[int],
        bridges: list[tuple[int, int]]
        ):
    
    global timer
    vis[node] = 1
    tin[node] = timer
    low[node] = timer
    timer+=1

    for (to, eid) in adj[node]:
        # skip the exact same edge we came from (identify by edge id)
        if eid == parent_eid:
            continue

        if vis[to] == 0:
            dfs_bridges(to, eid, vis, adj, tin, low, bridges)
            low[node] = min(low[node], low[to])

            if low[to] > tin[node]:
                # The edge is a bridge
                bridges.append((node, to))
        else:
            low[node] = min(low[node], low[to])

def get_bridges(adjecent_list):
    n = len(adjecent_list)

    bridges = []
    vis = [0]*n
    vis[0] = 1
    tin = [0]*n
    low = [0]*n

    dfs_bridges(0, -1, vis, adjecent_list, tin, low, bridges)

    return bridges


# def dfs_cycles(node, vis: set, traversed_nodes: set, adj, edge_count: set):
#     if node not in vis:
#         vis.add(node)
#         traversed_nodes.add(node)
#         for neighbor, eid in adj[node]:
#             if eid not in edge_count:      # count only once
#                 edge_count.add(eid)
#             dfs_cycles(neighbor, vis, traversed_nodes, adj, edge_count)
            

# def build_bridge_map(bridges):
#     mp = {}
#     for u, v in bridges:
#         mp.setdefault(u, []).append(v)
#         mp.setdefault(v, []).append(u)
#     return mp


# def get_compressed_cyclic_graph(bridges, adjecent_list):
#     no_bridges = adjecent_list.copy()
#     ends_of_bridges = set()
#     bridge_map = build_bridge_map(bridges)
#     for fr, to in bridges:
#         for i, (d, eid) in enumerate(no_bridges[fr]):
#             if d == to:
#                 del no_bridges[fr][i]
            

#         for i, (d, eid) in enumerate(no_bridges[to]):
#             if d == fr:
#                 del no_bridges[to][i]
        
#         ends_of_bridges.add(fr)
#         ends_of_bridges.add(to)

#     print()
#     print("NO BRIDGES")
#     for k, i in enumerate(no_bridges):
#         print(k, i)

#     new_adjecent = [[] for _ in range(len(adjecent_list))]

#     clumps: list[tuple[set, int]] = []
    
#     traversed_nodes = set()
#     for node, lis in enumerate(no_bridges):
#         if len(lis) == 0 or node in traversed_nodes: continue
#         vis = set()
#         edge_count = set()
#         dfs_cycles(node, vis, traversed_nodes, no_bridges, edge_count)
#         clumps.append((vis, len(edge_count)))


#     # Build the graph again with no EID
#     for c, edge_count in clumps:
        
#         # connection nodes of the cycle
#         connecting_nodes = ends_of_bridges.intersection(c)
#         compressed_node = random.choice(list(connecting_nodes))

#         # end of bridges from the specific cycle connection node
#         for connection in (connecting_nodes - set([compressed_node])):
#             other_end_bridge: list = bridge_map[connection]

#             # (connection, other_end_bridge[k]) is a single connection
#             # from compressed node to other a node out of the cycle
#             for other in other_end_bridge:
#                 new_adjecent[compressed_node].append(other)
        
#         # each edge in the cluster becomes a stick
#         for e in range(edge_count):
#             new_adjecent.append([])
#             new_adjecent[compressed_node].append(len(new_adjecent)-1)

#     for a,b in bridges:
#         new_adjecent[a].append(b)

#     return new_adjecent



def build_bridge_map(bridges):
    mp = {}
    for u, v in bridges:
        mp.setdefault(u, []).append(v)
        mp.setdefault(v, []).append(u)
    return mp

def get_compressed_cyclic_graph(bridges, adjecent_list):
    # make a deep-ish copy of adjacency so we can safely mutate
    no_bridges = [list(lst) for lst in adjecent_list]

    # remove bridge edges from the adjacency (safe removal via filter)
    for (u, v) in bridges:
        no_bridges[u] = [(d, eid) for (d, eid) in no_bridges[u] if d != v]
        no_bridges[v] = [(d, eid) for (d, eid) in no_bridges[v] if d != u]

    # helper to find cycles/components ignoring bridges
    def dfs_collect(start, no_bridges, visited, eids_seen):
        stack = [start]
        comp_nodes = set()
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            comp_nodes.add(node)
            for neigh, eid in no_bridges[node]:
                eids_seen.add(eid)
                if neigh not in visited:
                    stack.append(neigh)
        return comp_nodes

    # find components (clumps) and their edge counts (unique eids)
    visited = set()
    clumps = []             # list of (set_of_nodes, edge_count)
    for node in range(len(no_bridges)):
        if node in visited:
            continue
        # skip isolated (no edges) nodes here; they will remain as-is
        if not no_bridges[node]:
            visited.add(node)
            continue
        eids_seen = set()
        comp = dfs_collect(node, no_bridges, visited, eids_seen)
        clumps.append((comp, len(eids_seen)))

    # map each original node -> compressed node (by default itself)
    orig_to_compressed = {i: i for i in range(len(adjecent_list))}
    bridge_map = build_bridge_map(bridges)
    ends_of_bridges = set()
    for u, v in bridges:
        ends_of_bridges.add(u)
        ends_of_bridges.add(v)

    # Start new adjacency with one slot per original node (we'll append more)
    new_adjecent = [[] for _ in range(len(adjecent_list))]

    # For each cycle: choose a representative and map every node in the cycle to it.
    # Deterministic choice: smallest node in the component (you may change to random.choice)
    for comp_nodes, ecount in clumps:
        connecting_nodes = ends_of_bridges.intersection(comp_nodes)
        if not connecting_nodes:
            # if the cycle has no bridges attached, we still compress it to a single node
            # choose representative deterministically
            representative = min(comp_nodes)
        else:
            # choose representative deterministically among connecting nodes
            representative = min(connecting_nodes)
            

        # map all nodes in the component to representative
        for n in comp_nodes:
            orig_to_compressed[n] = representative

        # For every other connection node in the cycle, add edges from representative
        # to the external bridge endpoints that were connected to that connection node.
        for connection in (connecting_nodes - {representative}):
            for other in bridge_map.get(connection, []):
                # add edge representative -> other (we'll remap all bridges afterwards too)
                if other not in new_adjecent[representative]:
                    new_adjecent[representative].append(other)

        # now create stick nodes for each internal edge of the cluster.
        # each internal edge becomes its own leaf node attached to representative.
        for _ in range(ecount):
            new_node_index = len(new_adjecent)
            new_adjecent.append([])               # extend adjacency
            # undirected: connect both ways (representative <-> new leaf)
            new_adjecent[representative].append(new_node_index)
            new_adjecent[new_node_index].append(representative)

    # Finally, re-add all bridges, but using the mapping orig->compressed
    for a, b in bridges:
        A = orig_to_compressed.get(a, a)
        B = orig_to_compressed.get(b, b)
        if B not in new_adjecent[A]:
            new_adjecent[A].append(B)
        if A not in new_adjecent[B]:
            new_adjecent[B].append(A)

    # (Optional) remove self-loops if any (in case a and b mapped to same compressed node)
    for i in range(len(new_adjecent)):
        new_adjecent[i] = [x for x in new_adjecent[i] if x != i]


    start = orig_to_compressed[0]
    return new_adjecent, start


def shrub(node, tree: list, vis: set):
    if len(tree[node]) == 0:
        return 0
    vis.add(node)
    grundy_num = 0
    for child in tree[node]:
        if child not in vis:
            grundy_num ^= shrub(child, tree, vis) + 1 # plus one for each stick connecting to parent from child    
    return grundy_num

def main():
    n, m = map(int, input().split())
    n+=1

    adjecent = [[] for i in range(n)]

    eid = 0
    for _ in range(m):
        a, b = map(int, input().split())
        if a == -1:
            a = 0
        if b == -1:
            b = 0
        # add edge with an id to each adjacency list
        adjecent[a].append((b, eid))
        adjecent[b].append((a, eid))
        eid += 1

    # for k, i in enumerate(adjecent):
    #     print(k, i)

    bridges = get_bridges(adjecent)
    # print()
    # print('BRIDGES')
    # for i in bridges:
    #     print(min(i), max(i))


    # print()
    complete_graph = get_compressed_cyclic_graph(bridges, adjecent)
    # print()
    # print("COMPLETE GRAPH")
    # for k, i in enumerate(complete_graph):
    #     print(k, i)

    vis = set()
    vis.add(0)
    game_value = shrub(0, complete_graph, vis)
    print(f"*{game_value}")
    
    

main()