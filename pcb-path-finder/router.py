from typing import List, Set, Optional
from models import Component, Pin, Point
from collections import deque
import heapq
from visualizer import PathVisualizer
import matplotlib.pyplot as plt

def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def euclidean_distance(p1: Point, p2: Point) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

def find_route(components: Set[Component], start_pin: Pin, end_pin: Pin) -> List[Point]:
    # Create visualizer
    vis = PathVisualizer(components, start_pin, end_pin)
    path = []
    
    def is_valid_point(point: Point) -> bool:
        # Check if point is at least 1 unit away from all components
        for comp in components:
            if (comp.x <= point.x <= comp.x + comp.width and 
                comp.y <= point.y <= comp.y + comp.height):
                return False
        return True
    
    def get_neighbors(point: Point) -> List[Point]:
        # Only orthogonal movements (no diagonals)
        steps = [1, 2, 3, 5, 8]  # Variable step sizes
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Only horizontal and vertical
        neighbors = []
        
        for step in steps:
            for dx, dy in directions:
                new_point = Point(point.x + dx * step, point.y + dy * step)
                if (abs(new_point.x - start_pos.x) <= max_distance and 
                    abs(new_point.y - start_pos.y) <= max_distance and
                    is_valid_point(new_point)):
                    # Check if the path to the new point is clear
                    if all(is_valid_point(Point(
                        point.x + dx * i if dx != 0 else point.x,
                        point.y + dy * i if dy != 0 else point.y))
                        for i in range(1, step + 1)):
                        neighbors.append((new_point, step))
        
        if not neighbors:
            print(f"No valid neighbors found for point ({point.x}, {point.y})")
        return neighbors
    
    start_pos = start_pin.get_absolute_position()
    end_pos = end_pin.get_absolute_position()
    
    print(f"Searching for path from ({start_pos.x}, {start_pos.y}) to ({end_pos.x}, {end_pos.y})")
    print(f"Manhattan distance: {manhattan_distance(start_pos, end_pos)}")
    
    # Increase search distance
    max_distance = manhattan_distance(start_pos, end_pos) * 5
    
    # A* search
    counter = 0
    open_set = [(0, counter, start_pos)]
    came_from = {}
    g_score = {start_pos: 0.0}
    f_score = {start_pos: manhattan_distance(start_pos, end_pos)}  # Use manhattan for heuristic
    
    iterations = 0
    max_iterations = 100000
    
    while open_set and iterations < max_iterations:
        iterations += 1
        current = heapq.heappop(open_set)[2]
        
        # Update visualization more frequently
        if iterations % 50 == 0:
            vis.update(current, set(g_score.keys()), g_score, open_set, iterations, show=True)
        
        if iterations % 1000 == 0:
            print(f"Iteration {iterations}, explored {len(g_score)} points, queue size {len(open_set)}")
        
        if manhattan_distance(current, end_pos) < 2:  # Relax end condition slightly
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_pos)
            print(f"Path found after {iterations} iterations")
            path = path[::-1]
            path.append(end_pos)  # Add final point
            return path
        
        for neighbor, cost in get_neighbors(current):
            tentative_g_score = g_score[current] + cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + manhattan_distance(neighbor, end_pos)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))
    
    print(f"Path finding stopped after {iterations} iterations")
    print(f"Open set size: {len(open_set)}")
    print(f"Number of points explored: {len(g_score)}")
    
    vis.show_final_path(path)
    return path 