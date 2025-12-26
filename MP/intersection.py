import numpy as np
from numba import njit
import time

@njit
def point_inside_circles(x, y, circles):
    for i in range(circles.shape[0]):
        cx, cy, r = circles[i, 0], circles[i, 1], circles[i, 2]
        dx = x - cx
        dy = y - cy
        if dx*dx + dy*dy > r*r:
            return False
    return True

@njit
def monte_carlo(circles, n_samples, sample_circle):
    cx, cy, r = sample_circle
    inside = 0
    for _ in range(n_samples):
        # uniform inside circle
        theta = np.random.uniform(0, 2*np.pi)
        rr = r * np.sqrt(np.random.uniform())
        x = cx + rr * np.cos(theta)
        y = cy + rr * np.sin(theta)
        if point_inside_circles(x, y, circles):
            inside += 1
    return inside

def estimate_area(circles_list, n_samples=100000):
    circles = np.array([[cx, cy, r] for (cx, cy), r in circles_list])
    # pick circle near center as sample circle
    avg_x = np.mean(circles[:,0])
    avg_y = np.mean(circles[:,1])
    sample_circle_idx = np.argmin((circles[:,0]-avg_x)**2 + (circles[:,1]-avg_y)**2)
    sample_circle = circles[sample_circle_idx]
    inside = monte_carlo(circles, n_samples, sample_circle)
    sample_area = np.pi * sample_circle[2]**2
    return sample_area * inside / n_samples

def generate_test_circles(k, seed=None, ensure_intersection=True):
    """
    Generate k circles with centers in [-10000, 10000] and radii in [1, 20000]
    If ensure_intersection=True, generates circles that all intersect with substantial overlap
    """
    if seed is not None:
        np.random.seed(seed)
    
    circles = []
    
    if ensure_intersection:
        # Pick a central point where all circles will intersect
        center_x = np.random.randint(-5000, 5001)
        center_y = np.random.randint(-5000, 5001)
        
        # Generate circles clustered around this region for substantial overlap
        # Use smaller offsets and larger radii to create bigger intersection
        for _ in range(k):
            # Keep circles close together - smaller max_offset means more overlap
            # Scale based on k: fewer circles = can spread more, more circles = need tighter clustering
            if k <= 10:
                max_offset = 3000
                min_radius_base = 3000
                radius_range = 5000
            elif k <= 50:
                max_offset = 2000
                min_radius_base = 2500
                radius_range = 4000
            elif k <= 100:
                max_offset = 1500
                min_radius_base = 2000
                radius_range = 3000
            else:
                max_offset = 1000
                min_radius_base = 1500
                radius_range = 2500
            
            offset_x = np.random.randint(-max_offset, max_offset + 1)
            offset_y = np.random.randint(-max_offset, max_offset + 1)
            
            cx = center_x + offset_x
            cy = center_y + offset_y
            
            # Ensure circle stays within bounds
            cx = np.clip(cx, -10000, 10000)
            cy = np.clip(cy, -10000, 10000)
            
            # Distance from circle center to the common intersection point
            dist_to_center = np.sqrt(offset_x**2 + offset_y**2)
            
            # Use larger radii to ensure substantial overlap
            # Radius should be significantly larger than distance to center
            min_radius = max(int(dist_to_center * 1.5), min_radius_base)
            max_radius = min(min_radius + radius_range, 20000)
            
            if min_radius > max_radius:
                min_radius = max(1, max_radius - 1000)
            
            r = np.random.randint(min_radius, max_radius + 1)
            circles.append(((cx, cy), r))
    else:
        # Original random generation (may not intersect)
        for _ in range(k):
            cx = np.random.randint(-10000, 10001)
            cy = np.random.randint(-10000, 10001)
            r = np.random.randint(1, 20001)
            circles.append(((cx, cy), r))
    
    return circles

def print_circles(circles, limit=10):
    """Print circles in the input format"""
    print(f"{len(circles)}")
    for i, ((cx, cy), r) in enumerate(circles):
        if limit and i >= limit:
            print(f"  ... ({len(circles) - limit} more circles)")
            break
        print(f"{cx} {cy} {r}")

def run_tests():
    """
    Run tests with various numbers of circles and measure computation time
    """
    print("Monte Carlo Circle Intersection Area - Performance Tests")
    print("=" * 70)
    
    # Predefined test cases
    test_cases = [
        {
            "name": "Single circle",
            "circles": [((0, 0), 10)]
        },
        {
            "name": "Given example (3 circles)",
            "circles": [
                ((75, 83), 62),
                ((6, 62), 78),
                ((45, 89), 100)
            ],
            "expected": 5680.8875646107945934
        },
        {
            "name": "Test case 2 (3 circles)",
            "circles": [
                ((0, 0), 1),
                ((2, 0), 1),
                ((50, 50), 1000)
            ]
        },
        {
            "name": "Test case 3 (4 circles)",
            "circles": [
                ((19, 86), 68),
                ((34, 46), 54),
                ((87, 19), 68),
                ((94, 62), 65)
            ]
        },
        {
            "name": "Test case 4 (5 circles)",
            "circles": [
                ((-4, -7), 90),
                ((40, 30), 100),
                ((3, 4), 54),
                ((-6, 10), 70),
                ((0, -20), 80)
            ]
        },
        {
            "name": "Test case 5 (5 circles, small)",
            "circles": [
                ((0, 2), 3),
                ((0, 2), 2),
                ((2, 0), 2),
                ((0, -2), 2),
                ((-2, 0), 2)
            ]
        },
        {
            "name": "Test case 6 (5 circles)",
            "circles": [
                ((-16, 63), 65),
                ((-63, 16), 65),
                ((8, -57), 65),
                ((55, -10), 65),
                ((-4, 3), 5)
            ]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        circles = test['circles']
        
        print("\nInput circles:")
        print_circles(circles, limit=None)
        
        start = time.time()
        area = estimate_area(circles, n_samples=100000)
        elapsed = time.time() - start
        
        print(f"\n  Circles: {len(circles)}")
        print(f"  Estimated area: {area:.10f}")
        if "expected" in test:
            print(f"  Expected: {test['expected']}")
        print(f"  Time: {elapsed:.4f} seconds")
        
        if elapsed > 1.0:
            print(f"  WARNING: Exceeded 1 second time limit!")
    
    # Test different numbers of circles
    test_sizes = [10, 50, 100, 200, 500]
    
    print("\n" + "=" * 70)
    print("Tests with generated circles that all intersect:")
    
    for k in test_sizes:
        print(f"\nTest: {k} circles")
        circles = generate_test_circles(k, seed=42, ensure_intersection=True)
        
        print("\nInput circles (first 10):")
        print_circles(circles, limit=10)
        
        # Warm up numba
        if k == test_sizes[0]:
            _ = estimate_area(circles[:3], n_samples=1000)
        
        start = time.time()
        area = estimate_area(circles, n_samples=100000)
        elapsed = time.time() - start
        
        print(f"\n  Circles: {len(circles)}")
        print(f"  Estimated area: {area:.2f}")
        print(f"  Time: {elapsed:.4f} seconds")
        
        if elapsed > 1.0:
            print(f"  WARNING: Exceeded 1 second time limit!")
    
    # Test with maximum circles and adaptive sampling
    print("\n" + "=" * 70)
    print("Test: 500 circles with adaptive sampling")
    circles_max = generate_test_circles(500, seed=123, ensure_intersection=True)
    
    print("\nInput circles (first 10):")
    print_circles(circles_max, limit=10)
    
    # Try different sample sizes to stay under 1 second
    for n_samples in [10000, 50000, 100000, 200000]:
        start = time.time()
        area = estimate_area(circles_max, n_samples=n_samples)
        elapsed = time.time() - start
        print(f"\n  Samples: {n_samples}")
        print(f"  Estimated area: {area:.2f}")
        print(f"  Time: {elapsed:.4f} seconds")
        
        if elapsed > 1.0:
            print(f"  Exceeded 1 second - use fewer samples")
            break

if __name__ == "__main__":
    run_tests()