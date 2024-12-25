import random
import matplotlib.pyplot as plt
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set
import mplcursors
import heapq

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Pin:
    x: int
    y: int
    component: 'Component'  # Type hint for forward reference

@dataclass
class Component:
    x: int  # Lower-left corner x
    y: int  # Lower-left corner y
    width: int
    height: int
    pins: List[Pin]

    def get_perimeter_points(self) -> Set[Tuple[int, int]]:
        points = set()
        # Bottom and Top edges (excluding corners)
        for i in range(self.x + 1, self.x + self.width):
            points.add((i, self.y))
            points.add((i, self.y + self.height))
        # Left and Right edges (excluding corners)
        for j in range(self.y + 1, self.y + self.height):
            points.add((self.x, j))
            points.add((self.x + self.width, j))
        return points

def generate_random_components(num_components: int, min_size: int = 5, max_size: int = 20,
                              board_size: int = 100, min_spacing: int = 2) -> List[Component]:
    components = []
    attempts = 0
    while len(components) < num_components and attempts < num_components * 10:
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        x = random.randint(0, board_size - width)
        y = random.randint(0, board_size - height)
        new_component = Component(x, y, width, height, [])
        # Check spacing
        collision = False
        for comp in components:
            if not (new_component.x + new_component.width + min_spacing <= comp.x or
                    new_component.x >= comp.x + comp.width + min_spacing or
                    new_component.y + new_component.height + min_spacing <= comp.y or
                    new_component.y >= comp.y + comp.height + min_spacing):
                collision = True
                break
        if not collision:
            # Generate random pins on the perimeter, not on corners
            num_pins = random.randint(8, 30)
            perimeter = []
            for i in range(new_component.x + 1, new_component.x + new_component.width):
                perimeter.append((i, new_component.y))
                perimeter.append((i, new_component.y + new_component.height))
            for j in range(new_component.y + 1, new_component.y + new_component.height):
                perimeter.append((new_component.x, j))
                perimeter.append((new_component.x + new_component.width, j))
            # Ensure unique pin positions
            if len(perimeter) < num_pins:
                pins_positions = perimeter  # All available positions
            else:
                pins_positions = random.sample(perimeter, num_pins)
            for pos in pins_positions:
                pin = Pin(pos[0], pos[1], new_component)
                new_component.pins.append(pin)
            components.append(new_component)
        attempts += 1
    return components

def find_path_a_star(start_pin: Pin, end_pin: Pin, components: List[Component]) -> Optional[List[Point]]:
    """
    Implements the A* algorithm to find a path from start_pin to end_pin using horizontal and vertical segments.
    """
    start = (start_pin.x, start_pin.y)
    end = (end_pin.x, end_pin.y)

    # Create a set of blocked points (component interiors and perimeters)
    blocked = set()
    for comp in components:
        blocked.update(comp.get_perimeter_points())
        for i in range(comp.x + 1, comp.x + comp.width):
            for j in range(comp.y + 1, comp.y + comp.height):
                blocked.add((i, j))
    # Remove start and end points from blocked if they are on perimeters
    blocked.discard(start)
    blocked.discard(end)

    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_move_valid(prev_point: Tuple[int, int], current_point: Tuple[int, int]) -> bool:
        """
        Ensures that the move is perpendicular to the component perimeter if at the start or end.
        """
        # Implemented within move logic below
        return True  # Placeholder for additional constraints

    open_set = []
    heapq.heappush(open_set, (heuristic(start, end), 0, start, [Point(*start)]))
    visited = set()
    visited.add(start)

    while open_set:
        estimated_total, cost, current, path = heapq.heappop(open_set)
        if current == end:
            return path
        x, y = current
        # Explore neighbors: up, down, left, right
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for nx, ny in neighbors:
            if 0 <= nx <= 100 and 0 <= ny <= 100 and (nx, ny) not in blocked and (nx, ny) not in visited:
                # Perpendicular constraint for the first and last move
                if len(path) == 1:
                    # First move should be perpendicular to the start component perimeter
                    if start_pin.x == nx:
                        # Vertical move
                        if start_pin.component.y + start_pin.component.height == y:
                            pass
                        else:
                            continue
                    elif start_pin.y == ny:
                        # Horizontal move
                        if start_pin.component.x + start_pin.component.width == x:
                            pass
                        else:
                            continue
                if (nx, ny) == end:
                    # Last move should be perpendicular to the end component perimeter
                    if end_pin.x == nx:
                        # Vertical move
                        if end_pin.component.y + end_pin.component.height == ny:
                            pass
                        else:
                            continue
                    elif end_pin.y == ny:
                        # Horizontal move
                        if end_pin.component.x + end_pin.component.width == x:
                            pass
                        else:
                            continue
                visited.add((nx, ny))
                new_cost = cost + 1
                estimated = new_cost + heuristic((nx, ny), end)
                heapq.heappush(open_set, (estimated, new_cost, (nx, ny), path + [Point(nx, ny)]))
    return None

def visualize(components: List[Component], path: Optional[List[Point]] = None,
              start_pin: Optional[Pin] = None, end_pin: Optional[Pin] = None):
    """
    Visualizes the PCB layout, pins, and the routing path using matplotlib with interactive tooltips.
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw components
    for comp in components:
        rect = plt.Rectangle((comp.x, comp.y), comp.width, comp.height,
                             linewidth=1, edgecolor='black', facecolor='lightgray')
        ax.add_patch(rect)
        # Draw pins
        pin_x = [pin.x for pin in comp.pins]
        pin_y = [pin.y for pin in comp.pins]
        scatter_pins = ax.scatter(pin_x, pin_y, c='red', s=30, label='Pins')

    # Highlight start and end pins
    scatter_start = None
    scatter_end = None
    if start_pin:
        scatter_start = ax.scatter(start_pin.x, start_pin.y, c='green', s=150,
                                   marker='s', edgecolors='black', linewidth=2, label='Start Pin')
    if end_pin:
        scatter_end = ax.scatter(end_pin.x, end_pin.y, c='purple', s=150,
                                 marker='s', edgecolors='black', linewidth=2, label='End Pin')

    # Draw path if exists
    scatter_route = None
    if path and len(path) > 1:
        path_x = [point.x for point in path]
        path_y = [point.y for point in path]
        # Draw the main path
        scatter_route = ax.plot(path_x, path_y, marker='o', color='magenta',
                                linewidth=4, linestyle='-', label='Route')[0]
        # Add arrows to indicate direction
        for i in range(len(path_x) - 1):
            ax.arrow(path_x[i], path_y[i],
                     path_x[i+1] - path_x[i], path_y[i+1] - path_y[i],
                     length_includes_head=True, head_width=1.5, color='magenta')

        # Number the points with a contrasting color and larger font
        for idx, (x, y) in enumerate(zip(path_x, path_y)):
            ax.text(x, y, str(idx), color='yellow', fontsize=9, weight='bold',
                    bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.2'))

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal', adjustable='box')
    ax.legend(loc='upper right')
    plt.title('PCB Path Finder Visualization')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Add interactive tooltips using mplcursors
    all_pins = [pin for comp in components for pin in comp.pins]

    cursor_pins = mplcursors.cursor(scatter_pins, hover=True)
    if scatter_start:
        cursor_start = mplcursors.cursor(scatter_start, hover=True)
    if scatter_end:
        cursor_end = mplcursors.cursor(scatter_end, hover=True)

    @cursor_pins.connect("add")
    def on_add_pins(sel):
        idx = sel.target.index
        if idx < len(all_pins):
            pin = all_pins[idx]
            sel.annotation.set(text=f"Pin ({pin.x}, {pin.y})")

    if scatter_start:
        @cursor_start.connect("add")
        def on_add_start(sel):
            sel.annotation.set(text=f"Start Pin\n({start_pin.x}, {start_pin.y})")

    if scatter_end:
        @cursor_end.connect("add")
        def on_add_end(sel):
            sel.annotation.set(text=f"End Pin\n({end_pin.x}, {end_pin.y})")

    if scatter_route:
        cursor_route = mplcursors.cursor(scatter_route, hover=True)
        @cursor_route.connect("add")
        def on_add_route(sel):
            idx = sel.target.index
            if idx < len(path):
                point = path[idx]
                sel.annotation.set(text=f"Route Point {idx}\n({point.x}, {point.y})")

    plt.show()

def test_procedure():
    """
    Generates random components and pins, selects two random pins, finds a path, and visualizes it.
    """
    num_components = random.randint(20, 100)
    components = generate_random_components(num_components)
    if len(components) < 2:
        print("Not enough components generated.")
        return
    # Select two random pins from different components
    all_pins = [pin for comp in components for pin in comp.pins]
    if len(all_pins) < 2:
        print("Not enough pins generated.")
        return
    start_pin, end_pin = random.sample(all_pins, 2)
    # Ensure pins are from different components
    while end_pin.component == start_pin.component:
        end_pin = random.choice(all_pins)
    print(f"Finding path from Pin at ({start_pin.x}, {start_pin.y}) to Pin at ({end_pin.x}, {end_pin.y})")
    path = find_path_a_star(start_pin, end_pin, components)
    if path:
        print("Path found:")
        for point in path:
            print(f"({point.x}, {point.y})")
    else:
        print("No path found.")
    visualize(components, path, start_pin, end_pin)

if __name__ == "__main__":
    test_procedure() 