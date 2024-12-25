import random
from typing import List, Tuple
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
      return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Pin(Point):
    def __init__(self, x: int, y: int, component=None):
      super().__init__(x, y)
      self.component = component

class Component:
    def __init__(self, x: int, y: int, width: int, height: int, pins: List[Pin] = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pins = pins if pins else []

    def __repr__(self):
      return f"Component(x={self.x}, y={self.y}, width={self.width}, height={self.height}, pins={self.pins})"

def is_point_inside_component(point: Point, component: Component) -> bool:
    return (component.x < point.x < component.x + component.width and
            component.y < point.y < component.y + component.height)

def is_point_on_component_perimeter(point: Point, component: Component) -> bool:
    return (
      (point.x == component.x or point.x == component.x + component.width) and component.y <= point.y <= component.y + component.height or
      (point.y == component.y or point.y == component.y + component.height) and component.x <= point.x <= component.x + component.width
    )

def get_absolute_pin_location(pin: Pin, component: Component) -> Point:
    return Point(pin.x + component.x, pin.y + component.y)

def get_component_perimeter_points(component: Component) -> List[Point]:
    points = []
    # Corners
    points.append(Point(component.x, component.y))
    points.append(Point(component.x + component.width, component.y))
    points.append(Point(component.x + component.width, component.y + component.height))
    points.append(Point(component.x, component.y + component.height))

    # Top and bottom edges, excluding the corners
    for x in range(component.x+1, component.x + component.width):
        points.append(Point(x, component.y))
        points.append(Point(x, component.y+component.height))
    # Left and right edges, excluding the corners
    for y in range(component.y+1, component.y + component.height):
        points.append(Point(component.x, y))
        points.append(Point(component.x + component.width, y))

    return points

def does_line_segment_intersect_component(p1: Point, p2: Point, component: Component) -> bool:
    # Check if either point is within the component
    if is_point_inside_component(p1, component) or is_point_inside_component(p2, component):
        return True

    # Check if a horizontal line crosses vertical edges
    if p1.y == p2.y:
        if component.y < p1.y < component.y + component.height:
            if (p1.x < component.x < p2.x) or (p2.x < component.x < p1.x) or \
                (p1.x < component.x + component.width < p2.x) or (p2.x < component.x + component.width < p1.x):
                return True
    
    # Check if a vertical line crosses horizontal edges
    if p1.x == p2.x:
        if component.x < p1.x < component.x + component.width:
           if (p1.y < component.y < p2.y) or (p2.y < component.y < p1.y) or \
               (p1.y < component.y + component.height < p2.y) or (p2.y < component.y + component.height < p1.y):
                return True

    # Check if either of the line segment points are on the perimeter
    if is_point_on_component_perimeter(p1, component) or is_point_on_component_perimeter(p2, component):
       return True
    
    return False

def generate_random_component(min_width: int, max_width: int, min_height: int, max_height: int, min_pins: int, max_pins: int, existing_components: List[Component]) -> Component:
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    
    # keep trying new locations until a valid one is found
    while True:
        x = random.randint(10, 900 - width - 10)
        y = random.randint(10, 900 - height - 10)
        
        component = Component(x, y, width, height)
        valid = True
        
        for existing in existing_components:
          if is_component_too_close(component, existing):
            valid = False
            break
        
        if valid:
            break

    # Generate pins
    num_pins = random.randint(min_pins, max_pins)
    pins = []
    perimeter_points = get_component_perimeter_points(component)

    # remove corners
    perimeter_points = [p for p in perimeter_points if not (p.x == component.x and p.y == component.y)
                          and not (p.x == component.x + component.width and p.y == component.y)
                          and not (p.x == component.x + component.width and p.y == component.y + component.height)
                          and not (p.x == component.x and p.y == component.y + component.height)]

    pins = random.sample(perimeter_points, num_pins)
    pins = [Pin(p.x-component.x, p.y-component.y, component) for p in pins]

    component.pins = pins
    return component

def is_component_too_close(component1: Component, component2: Component) -> bool:
    # Check for overlap
    if (component1.x < component2.x + component2.width and
            component1.x + component1.width > component2.x and
            component1.y < component2.y + component2.height and
            component1.y + component1.height > component2.y):
          return True
        
    # Check if too close on the x axis
    if (component1.x - component2.x - component2.width < 2) and (component2.x - component1.x - component1.width < 2) and \
        (component1.y < component2.y + component2.height and component1.y+component1.height > component2.y):
      return True

    # Check if too close on the y axis
    if (component1.y - component2.y - component2.height < 2) and (component2.y - component1.y - component1.height < 2) and \
      (component1.x < component2.x + component2.width and component1.x+component1.width > component2.x):
      return True

    return False

def distance(point1: Point, point2: Point) -> float:
    return ((point2.x - point1.x)**2 + (point2.y - point1.y)**2)**0.5

def find_path(components: List[Component], pin1: Pin, pin2: Pin) -> List[Point]:
    start_point = get_absolute_pin_location(pin1, pin1.component)
    end_point = get_absolute_pin_location(pin2, pin2.component)

    queue = [([start_point], 0)]  # (path, cost)

    while queue:
        path, cost = queue.pop(0)
        current_point = path[-1]

        if current_point == end_point:
            return path

        # check for possible valid moves in the four directions
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            # generate new points in the applicable direction until reaching the edge of the screen
            for step in range(1,1000):
                next_point = Point(current_point.x + step*dx, current_point.y + step*dy)
                
                # only consider moves if they stay within the screen
                if next_point.x < 0 or next_point.x > 1000 or next_point.y < 0 or next_point.y > 1000:
                    break

                valid = True
                for component in components:
                    if does_line_segment_intersect_component(current_point, next_point, component):
                      valid = False
                      break

                if valid:
                    new_path = list(path)
                    new_path.append(next_point)
                    new_cost = cost + distance(current_point, next_point)
                    queue.append((new_path, new_cost))
                else:
                    break
        
        queue.sort(key=lambda item: item[1])  # Sort by cost

    return []  # No path found

def generate_test_data() -> Tuple[List[Component], Pin, Pin]:
    num_components = random.randint(20, 100)
    components = []
    for _ in range(num_components):
       component = generate_random_component(50, 150, 50, 150, 8, 30, components)
       components.append(component)
       
    # Select random pins
    all_pins = []
    for component in components:
      all_pins.extend(component.pins)
    
    if len(all_pins) < 2:
      raise Exception("Need at least two pins")
      
    pin1, pin2 = random.sample(all_pins, 2)
    
    return components, pin1, pin2

def draw_problem_and_result(components: List[Component], path: List[Point], pin1: Pin, pin2: Pin) -> None:
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Path Finding")

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add keyboard event to quit with ESC key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill((255, 255, 255))  # white background

        # Draw components
        for component in components:
            pygame.draw.rect(screen, (0, 0, 255), (component.x, component.y, component.width, component.height), 3)
            
            # Draw all pins for this component
            for pin in component.pins:
                abs_pin = get_absolute_pin_location(pin, component)
                pygame.draw.circle(screen, (0, 255, 0), (abs_pin.x, abs_pin.y), 3)

        # Draw path if it exists
        if path:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, (255, 0, 0), 
                               (path[i].x, path[i].y), 
                               (path[i+1].x, path[i+1].y), 3)

        # Draw start and end pins
        abs_pin1 = get_absolute_pin_location(pin1, pin1.component)
        abs_pin2 = get_absolute_pin_location(pin2, pin2.component)
        pygame.draw.circle(screen, (255, 0, 255), (abs_pin1.x, abs_pin1.y), 5)  # magenta
        pygame.draw.circle(screen, (255, 255, 0), (abs_pin2.x, abs_pin2.y), 5)  # yellow

        # Update display
        pygame.display.flip()

        # Control frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()

def test_pathfinding():
  try:
    components, pin1, pin2 = generate_test_data()
    path = find_path(components, pin1, pin2)

    print("Components:")
    for component in components:
       print(component)
       
    print(f"Starting Pin: {get_absolute_pin_location(pin1, pin1.component)}")
    print(f"Ending Pin: {get_absolute_pin_location(pin2, pin2.component)}")
    print(f"Path: {path}")
    
    draw_problem_and_result(components, path, pin1, pin2)

  except Exception as e:
     print (f"Error: {e}")


if __name__ == "__main__":
    test_pathfinding()

    