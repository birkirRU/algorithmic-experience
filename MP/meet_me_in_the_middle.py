import math
EPS = 1e-12

def square_euclidean(x1, y1, x2, y2):
    return sum([pow(x2-x1, 2), pow(y2-y1, 2)])

def main():
    x1, y1, r1 = map(float, input().split())
    x2, y2, r2 = map(float, input().split())
    
    # Calculate distance between centers
    d = math.sqrt(square_euclidean(x1, y1, x2, y2))
    
    # Handle the case when centers coincide
    if d == 0:
        # Same center
        if r1 == r2:
            print("their")  
        elif r1 > r2:
            # Circle 2 is inside circle 1
            print("their")
        else:
            # Circle 1 is inside circle 2
            print("our")
        return
    
    # Check for no intersection
    if d > r1 + r2 + EPS:  
        print("impossible")
        return
    
    # Check for containment (one circle inside another)
    if d + r2 <= r1 + EPS:  # Circle 2 inside Circle 1
        print("their")
        return
    
    if d + r1 <= r2 + EPS:  # Circle 1 inside Circle 2
        print("our")
        return
    
    # Check for tangent circles (single intersection point)
    if abs(d - (r1 + r2)) < EPS or abs(abs(r1 - r2) - d) < EPS:
        if abs(d - (r1 + r2)) < EPS:
            ratio = r1 / (r1 + r2)
            x = x1 + ratio * (x2 - x1)
            y = y1 + ratio * (y2 - y1)
        else:
            if r1 > r2:
                ratio = (r1 - r2) / d
                x = x1 + ratio * (x2 - x1)
                y = y1 + ratio * (y2 - y1)
            else:
                ratio = (r2 - r1) / d
                x = x2 + ratio * (x1 - x2)
                y = y2 + ratio * (y1 - y2)
        
        print("compromise")
        print(f"{x:.12f} {y:.12f}")
        return
    
    a = (r1*r1 - r2*r2 + d*d) / (2*d)
    h = math.sqrt(r1*r1 - a*a)
    
    xm = x1 + a * (x2 - x1) / d
    ym = y1 + a * (y2 - y1) / d
    
    xs1 = xm + h * (y2 - y1) / d
    ys1 = ym - h * (x2 - x1) / d
    
    xs2 = xm - h * (y2 - y1) / d
    ys2 = ym + h * (x2 - x1) / d
    
    points = [(xs1, ys1), (xs2, ys2)]
    points.sort(key=lambda p: (p[0], p[1]))
    
    
    print("compromises")
    print(f"{points[0][0]:.12f} {points[0][1]:.12f}")
    print(f"{points[1][0]:.12f} {points[1][1]:.12f}")


main()