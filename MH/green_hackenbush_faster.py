import sys
sys.setrecursionlimit(1 << 18)

# ---------- Tarjan bridges (with edge ids) ----------
def get_bridges(n_nodes, adj):
    n = n_nodes
    vis = [0]*n
    tin = [0]*n
    low = [0]*n
    timer = 1
    bridges = []

    # use recursion but local-binding for speed
    def dfs(u, parent_eid):
        nonlocal timer
        vis[u] = 1
        tin[u] = low[u] = timer
        timer += 1

        for v, eid in adj[u]:
            if eid == parent_eid:
                continue
            if not vis[v]:
                dfs(v, eid)

                low[u] = min(low[u], low[v])

                if low[v] > tin[u]:
                    bridges.append((u, v))
            else:
                low[u] = min(low[u], low[v])

    for i in range(n):
        if not vis[i]:
            dfs(i, -1)

    return bridges

# ---------- compress cycles (remove bridges) ----------
def get_compressed_cyclic_graph(n_nodes, adj, bridges):
    # make shallow-copy of adjacency lists (we don't touch inner tuples)
    no_bridges = [list(lst) for lst in adj]

    # remove bridge edges (by neighbor) in O(total degree) time overall
    # build set of bridge-pairs for quick check
    bridge_pairs = set()
    for u,v in bridges:
        if u <= v:
            bridge_pairs.add((u,v))
        else:
            bridge_pairs.add((v,u))

    for u in range(n_nodes):
        # filter adjacency, keep only edges that are not bridges
        lst = no_bridges[u]
        filtered = []
        for v,eid in lst:
            key = (u,v) if u <= v else (v,u)
            if key not in bridge_pairs:
                filtered.append((v,eid))
        no_bridges[u] = filtered

    # collect connected components in graph without bridge edges
    visited = [0]*n_nodes
    comp_list = []  # (set_of_nodes, set_of_eids)
    for i in range(n_nodes):
        if visited[i] or not no_bridges[i]:
            visited[i] = visited[i] or 0
            continue
        stack = [i]
        comp_nodes = []
        eids = set()
        visited[i] = 1
        while stack:
            u = stack.pop()
            comp_nodes.append(u)
            for v,eid in no_bridges[u]:
                eids.add(eid)
                if not visited[v]:
                    visited[v] = 1
                    stack.append(v)
        comp_list.append((comp_nodes, eids))

    # map original node -> compressed representative (default itself)
    orig_to_comp = list(range(n_nodes))

    # determine which nodes are ends of bridges
    bridge_map = {}
    ends_of_bridges = set()
    for u,v in bridges:
        bridge_map.setdefault(u, []).append(v)
        bridge_map.setdefault(v, []).append(u)
        ends_of_bridges.add(u); ends_of_bridges.add(v)

    # Build new adjacency using sets for O(1) adds
    new_adj_sets = [set() for _ in range(n_nodes)]

    for comp_nodes, eids in comp_list:

        connecting_nodes = [x for x in comp_nodes if x in ends_of_bridges]
        if connecting_nodes:
            representative = min(connecting_nodes)  # deterministic
        else:
            representative = min(comp_nodes)
        # map all nodes in comp to representative
        for x in comp_nodes:
            orig_to_comp[x] = representative

        # For each connection node in the comp (except rep), create edges rep -> external targets
        for connection in connecting_nodes:
            if connection == representative:
                continue
            for other in bridge_map.get(connection, ()):
                new_adj_sets[representative].add(other)
                new_adj_sets[other].add(representative)

        # for each internal edge (unique eid) create a leaf attached to representative
        for _ in eids:
            new_node = len(new_adj_sets)
            new_adj_sets.append(set())
            new_adj_sets[representative].add(new_node)
            new_adj_sets[new_node].add(representative)

    # re-add bridges using mapped reps
    for u,v in bridges:
        U = orig_to_comp[u]
        V = orig_to_comp[v]
        if U != V:
            new_adj_sets[U].add(V)
            new_adj_sets[V].add(U)

    # convert sets to lists for downstream processing
    new_adj = [list(sorted(s)) for s in new_adj_sets]
    start = orig_to_comp[0]
    return new_adj, start

# ---------- compute Grundy on tree-like structure ----------
def compute_shrub_grundy(root, tree_adj):
    n = len(tree_adj)
    vis = bytearray(n)  # faster than set
    # recursion with local-binding for speed
    def dfs(u):
        vis[u] = 1
        g = 0
        for v in tree_adj[u]:
            if not vis[v]:
                gv = dfs(v) + 1
                g ^= gv
        return g
    return dfs(root)

# ---------- main ----------
def main():
    n, m = map(int, input().split())
    n+=1
    # input maps -1 -> 0 and nodes 1..n_read; 
    # We will set number of nodes = n_read + 1 to keep same indexing
    # build adjacency (undirected) with eid
    adj = [[] for i in range(n)]

    eid = 0
    for _ in range(m):
        a, b = map(int, input().split())
        if a == -1:
            a = 0
        if b == -1:
            b = 0
        # add edge with an id to each adjacency list
        adj[a].append((b, eid))
        adj[b].append((a, eid))
        eid += 1

    bridges = get_bridges(n, adj)
    compressed, start = get_compressed_cyclic_graph(n, adj, bridges)

    g = compute_shrub_grundy(start, compressed)
    print(f"*{g}")

if __name__ == "__main__":
    main()
