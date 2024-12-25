from dataclasses import dataclass
from typing import List, Set
from random import randint, uniform

@dataclass
class Point:
    x: int
    y: int
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

@dataclass
class Pin:
    x: int  # relative to component
    y: int  # relative to component
    component: 'Component'
    
    def get_absolute_position(self) -> Point:
        return Point(
            self.component.x + self.x,
            self.component.y + self.y
        )
    
    def __eq__(self, other):
        if not isinstance(other, Pin):
            return False
        return (self.x == other.x and 
                self.y == other.y and 
                self.component == other.component)
    
    def __hash__(self):
        return hash((self.x, self.y, id(self.component)))

@dataclass
class Component:
    x: int  # lower-left corner x
    y: int  # lower-left corner y
    width: int
    height: int
    pins: Set[Pin]
    
    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        return (self.x == other.x and 
                self.y == other.y and 
                self.width == other.width and 
                self.height == other.height)
    
    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))
    
    def contains_point(self, point: Point) -> bool:
        return (self.x <= point.x <= self.x + self.width and 
                self.y <= point.y <= self.y + self.height)
    
    def intersects_segment(self, p1: Point, p2: Point) -> bool:
        # Only handles horizontal or vertical segments
        if p1.x == p2.x:  # Vertical segment
            x = p1.x
            y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)
            return (self.x <= x <= self.x + self.width and
                    not (y_max < self.y or y_min > self.y + self.height))
        else:  # Horizontal segment
            y = p1.y
            x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
            return (self.y <= y <= self.y + self.height and
                    not (x_max < self.x or x_min > self.x + self.width)) 