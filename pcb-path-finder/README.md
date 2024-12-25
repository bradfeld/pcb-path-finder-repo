# PCB Path Finder

A Python implementation of a path-finding algorithm for PCB routing between components.

## Features
- Finds paths between pins on different components
- Ensures paths only use horizontal and vertical segments
- Avoids component collisions
- Includes visualization of components and routing

## Requirements
- Python 3.7+
- matplotlib

## Inspiration: From the following prompt from Dave Jilk

Fully implemented in Cursor using the AI Composer Feature.

Write a function that accepts as input, first, an unordered collection of objects called Components, each of which contains an unordered collection of Pins, and second, reference to two distinct Pins among all those. Each Component is a rectangle located on the Euclidean plane and has a specified height and width, with its placement in the plane specified as x and y values designating the location of the lower-left corner of the Component. Components are guaranteed not to overlap and to have at least two coordinate units between their perimeter and the perimeter of every other Component. The Pins of a Component are locations on the perimeter of the Component, guaranteed not to be on the corners, and specified as x and y values relative to the lower-left corner of the Component.

The output of the function is an ordered sequence of Points, each of which contains x and y coordinates indicating its location in the plane. The first Point in the sequence should be at the same location as the first Pin in the input, and the last Point in the sequence should be at the same location as the second Pin in the input. The line segment between any two Points in the returned sequence must always be horizontal or vertical, i.e., either the x or the y values between the two points are equal. Crucially, no line segment between two Points in the output can overlap with any Component, neither its interior nor its perimeter. The first and last line segments between the Points in the sequence must be perpendicular to the perimeter of the Component where the applicable input Pins are located. Finally, fewer Points and less total length of line segments between the Points is preferred, but optimality is not required and compute time is relevant.

Any data structure appropriate for the inputs and outputs is acceptable. All coordinate values should be signed long integers.

Also include a test procedure that generates a random set of 20 to 100 Components, each with a random number of Pins between 8 and 30 at random locations on the Component perimeter. Randomly specify a location for each Component, while still meeting the overlap and spacing guarantees given in the specification. Pick two Pins at random and run the function on this test data. If you can draw the problem and the result on the screen, that would be great.
