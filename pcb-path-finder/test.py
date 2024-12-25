import random
import matplotlib.pyplot as plt
from models import Component, Pin, Point
from router import find_route
from typing import Set, Tuple, List

def generate_test_case() -> Tuple[Set[Component], Pin, Pin]:
    components = set()
    all_pins = []
    
    # Generate random components
    num_components = random.randint(10, 50)  # Reduced from 20-100
    grid_size = int(num_components * 1.0)
    
    def generate_component_location() -> Tuple[int, int]:
        while True:
            x = random.randint(0, grid_size * 5)
            y = random.randint(0, grid_size * 5)
            width = random.randint(3, 10)   # Reduced from 5-15
            height = random.randint(3, 10)  # Reduced from 5-15
            
            # Check if location is valid (no overlap with existing components)
            valid = True
            for comp in components:
                if (abs(x - comp.x) < width + comp.width + 2 and 
                    abs(y - comp.y) < height + comp.height + 2):
                    valid = False
                    break
            
            if valid:
                return x, y, width, height
    
    # Create components with random pins
    for _ in range(num_components):
        x, y, width, height = generate_component_location()
        
        # Create the component first with an empty set of pins
        component = Component(x, y, width, height, set())
        components.add(component)
        
        # Generate random pins on perimeter
        num_pins = random.randint(8, 30)
        for _ in range(num_pins):
            # Randomly choose which side to place the pin
            side = random.randint(0, 3)
            if side == 0:  # Bottom
                pin_x = random.randint(1, width-1)
                pin_y = 0
            elif side == 1:  # Right
                pin_x = width
                pin_y = random.randint(1, height-1)
            elif side == 2:  # Top
                pin_x = random.randint(1, width-1)
                pin_y = height
            else:  # Left
                pin_x = 0
                pin_y = random.randint(1, height-1)
            
            # Create pin with reference to component immediately
            new_pin = Pin(pin_x, pin_y, component)
            component.pins.add(new_pin)
            all_pins.append(new_pin)
    
    # Select two random pins
    start_pin, end_pin = random.sample(all_pins, 2)
    
    return components, start_pin, end_pin

def visualize_result(components: Set[Component], start_pin: Pin, end_pin: Pin, path: List[Point]):
    plt.figure(figsize=(12, 12))
    
    # Draw components
    for comp in components:
        plt.gca().add_patch(plt.Rectangle(
            (comp.x, comp.y), comp.width, comp.height,
            fill=False, color='blue'
        ))
        
        # Draw pins
        for pin in comp.pins:
            abs_pos = pin.get_absolute_position()
            plt.plot(abs_pos.x, abs_pos.y, 'ro', markersize=3)
    
    # Highlight start and end pins
    start_pos = start_pin.get_absolute_position()
    end_pos = end_pin.get_absolute_position()
    plt.plot(start_pos.x, start_pos.y, 'go', markersize=6)
    plt.plot(end_pos.x, end_pos.y, 'ro', markersize=6)
    
    # Draw path
    if path:
        path_x = [p.x for p in path]
        path_y = [p.y for p in path]
        plt.plot(path_x, path_y, 'g-', linewidth=2)
    
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def main():
    # Generate and solve test case
    components, start_pin, end_pin = generate_test_case()
    path = find_route(components, start_pin, end_pin)
    
    if path:
        print(f"Path found with {len(path)} points")
        visualize_result(components, start_pin, end_pin, path)
    else:
        print("No path found")

if __name__ == "__main__":
    main() 