def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def get_convex_hull(points):
    n = len(points)
    if n <= 1:
        return points
    
    # lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]


def get_min_rotation(hull):
    if len(hull) == 2:
        a, b = hull[0][2], hull[1][2]
        return [hull[0], hull[1]] if a < b else [hull[1], hull[0]]
    
    # find minimum (x, y) point
    min_x = hull[0][0]
    min_y = hull[0][1]
    for p in hull:
        if p[0] < min_x or (p[0] == min_x and p[1] < min_y):
            min_x, min_y = p[0], p[1]
    
    # find all positions with that (x, y)
    positions = []
    for i, p in enumerate(hull):
        if p[0] == min_x and p[1] == min_y:
            positions.append(i)
    
    # pick smallest index among them
    best = positions[0]
    for i in positions[1:]:
        if hull[i][2] < hull[best][2]:
            best = i
    
    return hull[best:] + hull[:best]


def main():
    n = int(input())
    points = []
    
    for i in range(n):
        x, y = map(int, input().split())
        points.append((x, y, i + 1))
    
    points.sort()
    
    # remove duplicates, keep first index
    unique = []
    for p in points:
        if not unique or (p[0], p[1]) != (unique[-1][0], unique[-1][1]):
            unique.append(p)
    
    points = unique
    
    if len(points) == 1:
        print(1)
        print(points[0][2])
        return
    
    hull = get_convex_hull(points)
    hull = get_min_rotation(hull)
    
    print(len(hull))
    print(" ".join(str(p[2]) for p in hull))

main()