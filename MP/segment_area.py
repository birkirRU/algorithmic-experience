import math

def square_euclidean(x1, y1, x2, y2):
    return sum([pow(x2-x1, 2), pow(y2-y1, 2)])

def main():
    x, y, r = map(float, input().split())
    xa, ya = map(float, input().split())
    xb, yb = map(float, input().split())

    if r == 0:
        # No circle means no segment area
        print(0)
        return

    if (xa == 0 and ya == 0) or (xb == 0 and yb == 0):
        # No valid ray means no segment area
        print(0)
        return 
    # Normalize direction vectors
    da = math.sqrt(xa*xa + ya*ya)
    db = math.sqrt(xb*xb + yb*yb) 


    # scale unit vector with r to get the intersection of P and Ray A
    xp = x + (xa/da) * r
    yp = y + (ya/da) * r
    
    # scale unit vector with r to get the intersection of Q and Ray B
    xq = x + (xb/db) * r
    yq = y + (yb/db) * r
    
    # vectors (sides) from center to P and Q
    vp_x = xp - x
    vp_y = yp - y
    vq_x = xq - x
    vq_y = yq - y
    
    # angle between OP and OQ using dot product
    dot_product = vp_x * vq_x + vp_y * vq_y
    norm_p = math.sqrt(vp_x*vp_x + vp_y*vp_y)
    norm_q = math.sqrt(vq_x*vq_x + vq_y*vq_y)
    
    # cosine rule applied
    cos_theta = dot_product / (norm_p * norm_q)
    
    cos_theta = max(-1.0, min(1.0, cos_theta))
    
    # angle between the two rays in radians
    theta = math.acos(cos_theta)
    
    # We need the clockwise arc from P to Q
    # cross product to determine orientation
    cross_product = vp_x * vq_y - vp_y * vq_x
    
    # If cross product is positive, Q is counterclockwise from P
    # If negative, Q is clockwise from P
    # We need the clockwise arc, so if 'cross > theta', we need 2pi - theta
    if cross_product > 0:
        theta = 2 * math.pi - theta
    # If 'cross < theta', theta already gives clockwise angle
    
    # Area of circular segment
    # Segment area = (1/2) * r^2 * (theta - sin(theta)) = whole arc - triangle
    area = 0.5 * r * r * (theta - math.sin(theta))
    
    print(f"{area:.12f}")

main()