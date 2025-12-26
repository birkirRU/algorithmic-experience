import sys
sys.setrecursionlimit(1000000)
def grundy_num(nimbers):
    grundy_num = 0
    for ni in nimbers:
        grundy_num ^= ni
    return grundy_num

def shrub(node):
    if len(tree[node]) == 0:
        return 0 
    grundy_num = 0
    for child in tree[node]:
        grundy_num ^= shrub(child) + 1 # plus one for each stick connecting to parent from child    
    return grundy_num

n = int(input())

edges = list(map(int, input().split()))

# a full tree, where each vertex is connected |V| = E+1 vertecies exist
tree = [[] for i in range(n+1)]

for i, parent in enumerate(edges, 1):  # i is edge number (1-indexed)
    if parent == -1:
        # Edge i is attached to ground (0)
        tree[0].append(i)
    else:
        # Edge i is attached to parent edge
        tree[parent].append(i)

print(f"*{shrub(0)}")