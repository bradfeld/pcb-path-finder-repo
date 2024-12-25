# PCB Path Finder

A Python implementation of a path-finding algorithm for PCB routing between components.

## Features
- Finds paths between pins on different components
- Ensures paths only use horizontal and vertical segments
- Avoids component collisions
- Includes visualization of components and routing with interactive tooltips

## Requirements
- Python 3.7+
- matplotlib
- mplcursors

## Inspiration: From the following prompt from Dave Jilk

Fully implemented in Cursor using the AI Composer Feature with the o1-mini Model

Write a function that accepts as input, first, an unordered collection of objects called Components, each of which contains an unordered collection of Pins, and second, reference to two distinct Pins among all those. Each Component is a rectangle located on the Euclidean plane and has a specified height and width, with its placement in the plane specified as x and y values designating the location of the lower-left corner of the Component. Components are guaranteed not to overlap and to have at least two coordinate units between their perimeter and the perimeter of every other Component. The Pins of a Component are locations on the perimeter of the Component, guaranteed not to be on the corners, and specified as x and y values relative to the lower-left corner of the Component.

The output of the function is an ordered sequence of Points, each of which contains x and y coordinates indicating its location in the plane. The first Point in the sequence should be at the same location as the first Pin in the input, and the last Point in the sequence should be at the same location as the second Pin in the input. The line segment between any two Points in the returned sequence must always be horizontal or vertical, i.e., either the x or the y values between the two points are equal. Crucially, no line segment between two Points in the output can overlap with any Component, neither its interior nor its perimeter. The first and last line segments between the Points in the sequence must be perpendicular to the perimeter of the Component where the applicable input Pins are located. Finally, fewer Points and less total length of line segments between the Points is preferred, but optimality is not required and compute time is relevant.

Any data structure appropriate for the inputs and outputs is acceptable. All coordinate values should be signed long integers.

Also include a test procedure that generates a random set of 20 to 100 Components, each with a random number of Pins between 8 and 30 at random locations on the Component perimeter. Randomly specify a location for each Component, while still meeting the overlap and spacing guarantees given in the specification. Pick two Pins at random and run the function on this test data. If you can draw the problem and the result on the screen, that would be great.

## Running the Program

1. **Install Dependencies**:
    Ensure you have Python 3.7+ installed. Install the required libraries using pip:

    ```bash
    pip install matplotlib mplcursors
    ```
    
2. **Execute the Program**:
    Run the `main.py` script:

    ```bash
    python main.py
    ```

    The program will generate random components and pins, attempt to find a path between two randomly selected pins, and display an interactive visualization of the setup and the path. Hover over the pins and route points to see their coordinates and other details.

## Interactive Visualization

- **Pins**: Hover over red pins to view their coordinates.
- **Start Pin**: Hover over the green square to see "Start Pin" and its coordinates.
- **End Pin**: Hover over the purple square to see "End Pin" and its coordinates.
- **Route Points**: Hover over magenta route points to view their index and coordinates.

## Notes

- The path-finding algorithm implemented here is a simple BFS and may not be the most efficient for larger boards or more complex component arrangements. For improved performance and optimal paths, more advanced algorithms like A* with heuristics can be implemented.
- The visualization uses a fixed board size of 100x100 units. Adjust `board_size` in the `generate_random_components` function if needed.
- Ensure that the randomly generated components have enough space to allow for pathfinding between pins.

## Bugs
- It doesn't show the path
- The interactive tooltips don't seem to work
- A legend on the right with repeating "Pins" shows up vertically
