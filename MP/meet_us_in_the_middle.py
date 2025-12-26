import math
import sys

EPS = 1e-9

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def point_equal(p1, p2, eps=1e-7):
    """Check if two points are approximately equal"""
    return abs(p1[0] - p2[0]) < eps and abs(p1[1] - p2[1]) < eps

def normalize_angle(angle):
    """Normalize angle to [0, 2π)"""
    while angle < 0:
        angle += 2 * math.pi
    while angle >= 2 * math.pi:
        angle -= 2 * math.pi
    return angle

def circle_intersection(x1, y1, r1, x2, y2, r2):
    """Return intersection points of two circles, or empty list if none"""
    d = dist((x1, y1), (x2, y2))
    
    # No intersection or one circle contains the other
    if d > r1 + r2 + EPS or d < abs(r1 - r2) - EPS:
        return []
    
    # Same center
    if d < EPS and abs(r1 - r2) < EPS:
        return []
    
    a = (r1*r1 - r2*r2 + d*d) / (2*d)
    h2 = r1*r1 - a*a
    if h2 < -EPS:
        return []
    
    h = math.sqrt(max(0.0, h2))
    xm = x1 + a*(x2 - x1)/d
    ym = y1 + a*(y2 - y1)/d
    
    # Two intersection points
    point1 = (xm + h*(y2 - y1)/d, ym - h*(x2 - x1)/d)
    point2 = (xm - h*(y2 - y1)/d, ym + h*(x2 - x1)/d)
    
    return [point1, point2]

def check_point_in_all_circles(point, circles):
    """Check if a point is within all circles, and return list of circle indices that it's exactly on"""
    xp, yp = point
    on_boundary = []
    
    for xc, yc, rc, idx in circles:
        d = dist((xp, yp), (xc, yc))
        if d > rc + EPS:
            return None  # Point not in this circle
        if abs(d - rc) <= EPS:
            on_boundary.append(idx)
    
    return sorted(on_boundary)

def find_contained_disc(circles):
    """Check if any circle is completely contained within all others"""
    n = len(circles)
    for i in range(n):
        xi, yi, ri, idx = circles[i]
        ok = True
        for j in range(n):
            if i == j:
                continue
            xj, yj, rj, _ = circles[j]
            if dist((xi, yi), (xj, yj)) + ri > rj + EPS:
                ok = False
                break
        if ok:
            return idx
    return None

def collect_intersection_points(circles):
    """Collect all valid intersection points that are within all circles"""
    points = []
    n = len(circles)
    
    # Map from circle index to its data
    circle_dict = {idx: (x, y, r) for x, y, r, idx in circles}
    
    # Store intersection points by the pair of circles that create them
    point_dict = {}  # (frozenset(voters)) -> list of points
    
    for i in range(n):
        x1, y1, r1, idx1 = circles[i]
        for j in range(i + 1, n):
            x2, y2, r2, idx2 = circles[j]
            
            # Get intersection points between these two circles
            intersections = circle_intersection(x1, y1, r1, x2, y2, r2)
            
            for point in intersections:
                # Check if point is within all circles
                voters = check_point_in_all_circles(point, circles)
                if voters is not None and len(voters) >= 2:
                    # Sort voters
                    voters_tuple = tuple(sorted(voters))
                    
                    # Add to dictionary
                    key = voters_tuple
                    if key not in point_dict:
                        point_dict[key] = []
                    point_dict[key].append((point[0], point[1], voters_tuple))
    
    # For each set of voters, sort their points by orientation
    for voters_tuple, pts in point_dict.items():
        if len(pts) == 2:
            # Two points with same voters - need to order them
            x1, y1, _ = pts[0]
            x2, y2, _ = pts[1]
            
            # Get first voter's circle
            first_voter_idx = voters_tuple[0]
            xc, yc, rc = circle_dict[first_voter_idx]
            
            # Calculate angles relative to first voter's center
            angle1 = math.atan2(y1 - yc, x1 - xc)
            angle2 = math.atan2(y2 - yc, x2 - xc)
            
            # Normalize angles to [0, 2π)
            angle1 = normalize_angle(angle1)
            angle2 = normalize_angle(angle2)
            
            # Counter-clockwise order means increasing angle
            # But we want the one on the left (counter-clockwise) first
            # So sort by angle in ascending order
            if angle1 > angle2:
                pts[0], pts[1] = pts[1], pts[0]
        
        # Add all points
        for pt in pts:
            points.append(pt)
    
    return points

def deduplicate_points(points):
    """Remove duplicate points (within tolerance)"""
    if not points:
        return []
    
    # Sort to group similar points
    points.sort(key=lambda p: (p[2], p[0], p[1]))
    
    unique_points = []
    for point in points:
        x, y, voters = point
        if not unique_points or not point_equal((x, y), (unique_points[-1][0], unique_points[-1][1])):
            unique_points.append(point)
    
    return unique_points

def sort_points_for_output(points):
    """Sort points according to problem requirements"""
    if not points:
        return []
    
    # Group points by their voters
    points_by_voters = {}
    for x, y, voters in points:
        if voters not in points_by_voters:
            points_by_voters[voters] = []
        points_by_voters[voters].append((x, y, voters))
    
    # Sort voters lexicographically
    sorted_voters = sorted(points_by_voters.keys())
    
    # Build final sorted list
    sorted_points = []
    for voters in sorted_voters:
        pts = points_by_voters[voters]
        if len(pts) == 1:
            sorted_points.append(pts[0])
        else:
            # Points already sorted by orientation in collect_intersection_points
            sorted_points.extend(pts)
    
    return sorted_points

def main():
    n = int(sys.stdin.readline())
    circles = []
    
    for i in range(n):
        x, y, r = map(float, sys.stdin.readline().split())
        circles.append((x, y, r, i + 1))
    
    # Check for contained disc
    contained_idx = find_contained_disc(circles)
    if contained_idx is not None:
        print(f"voter {contained_idx}")
        return
    
    # Collect intersection points
    points = collect_intersection_points(circles)
    
    if not points:
        print("impossible")
        return
    
    # Deduplicate and sort
    unique_points = deduplicate_points(points)
    sorted_points = sort_points_for_output(unique_points)
    
    # Output
    print(f"compromise {len(sorted_points)}")
    for x, y, voters in sorted_points:
        # Clean up near-zero values
        if abs(x) < 1e-10:
            x = 0.0
        if abs(y) < 1e-10:
            y = 0.0
        print(f"{x:.16f} {y:.16f}", *voters)

if __name__ == "__main__":
    main()