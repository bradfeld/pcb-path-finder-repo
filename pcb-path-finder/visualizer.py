import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from models import Component, Pin, Point
from typing import Set, List, Dict, Optional
import numpy as np

class PathVisualizer:
    def __init__(self, components: Set[Component], start_pin: Pin, end_pin: Pin):
        self.components = components
        self.start_pin = start_pin
        self.end_pin = end_pin
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(20, 10))
        self.explored_points: Set[Point] = set()
        self.current_path: List[Point] = []
        
        # Calculate bounds
        self.min_x = min(comp.x for comp in components)
        self.min_y = min(comp.y for comp in components)
        self.max_x = max(comp.x + comp.width for comp in components)
        self.max_y = max(comp.y + comp.height for comp in components)
        
        # Add padding
        padding = max(self.max_x - self.min_x, self.max_y - self.min_y) * 0.1
        self.min_x = int(self.min_x - padding)
        self.min_y = int(self.min_y - padding)
        self.max_x = int(self.max_x + padding)
        self.max_y = int(self.max_y + padding)
        
        self.setup_plot()
        
    def setup_plot(self):
        # Setup main plot
        self.ax1.set_title("Path Finding Progress")
        self.ax1.set_xlim(self.min_x, self.max_x)
        self.ax1.set_ylim(self.min_y, self.max_y)
        self.ax1.grid(True)
        
        # Setup heatmap plot
        self.ax2.set_title("Exploration Density")
        self.ax2.set_xlim(self.min_x, self.max_x)
        self.ax2.set_ylim(self.min_y, self.max_y)
        
        # Draw components
        for comp in self.components:
            # Draw component
            rect = Rectangle((comp.x, comp.y), comp.width, comp.height,
                           fill=False, color='blue', linewidth=2)
            self.ax1.add_patch(rect)
            self.ax2.add_patch(Rectangle((comp.x, comp.y), comp.width, comp.height,
                                       fill=True, color='gray'))
            
            # Draw pins
            for pin in comp.pins:
                pos = pin.get_absolute_position()
                self.ax1.plot(pos.x, pos.y, 'r.', markersize=3)
        
        # Highlight start and end pins
        start_pos = self.start_pin.get_absolute_position()
        end_pos = self.end_pin.get_absolute_position()
        self.ax1.plot(start_pos.x, start_pos.y, 'go', markersize=10, label='Start')
        self.ax1.plot(end_pos.x, end_pos.y, 'ro', markersize=10, label='End')
        self.ax1.legend()
        
        # Initialize heatmap data
        self.grid_size = 100
        self.heatmap_data = np.zeros((self.grid_size, self.grid_size))
        
    def update(self, current_point: Point, explored_points: Set[Point], 
               g_scores: Dict[Point, float], open_set: List[tuple], 
               iteration: int, show: bool = False):
        self.explored_points.update(explored_points)
        
        # Update main plot
        self.ax1.cla()
        self.setup_plot()
        
        # Draw explored points
        x_coords = [p.x for p in self.explored_points]
        y_coords = [p.y for p in self.explored_points]
        self.ax1.plot(x_coords, y_coords, 'c.', markersize=1, alpha=0.3, label='Explored')
        
        # Draw current point
        if current_point:
            self.ax1.plot(current_point.x, current_point.y, 'y*', markersize=15, 
                         label='Current')
        
        # Draw open set
        if open_set:
            open_points = [point for _, _, point in open_set]
            x_coords = [p.x for p in open_points]
            y_coords = [p.y for p in open_points]
            self.ax1.plot(x_coords, y_coords, 'm.', markersize=3, label='Frontier')
        
        self.ax1.legend()
        
        # Update heatmap
        if explored_points:
            x_coords = np.array([p.x for p in explored_points])
            y_coords = np.array([p.y for p in explored_points])
            
            # Normalize coordinates to grid size
            x_norm = ((x_coords - self.min_x) / (self.max_x - self.min_x) * (self.grid_size - 1)).astype(int)
            y_norm = ((y_coords - self.min_y) / (self.max_y - self.min_y) * (self.grid_size - 1)).astype(int)
            
            # Clip to valid indices
            x_norm = np.clip(x_norm, 0, self.grid_size - 1)
            y_norm = np.clip(y_norm, 0, self.grid_size - 1)
            
            # Update heatmap
            for x, y in zip(x_norm, y_norm):
                self.heatmap_data[y, x] += 1
        
        self.ax2.cla()
        self.ax2.set_title("Exploration Density")
        self.ax2.imshow(self.heatmap_data, extent=[self.min_x, self.max_x, 
                                                  self.min_y, self.max_y],
                       origin='lower', cmap='hot', aspect='auto')
        
        # Add text information
        info_text = f"Iteration: {iteration}\n"
        info_text += f"Explored Points: {len(explored_points)}\n"
        info_text += f"Open Set Size: {len(open_set)}\n"
        info_text += f"Current g-score: {g_scores.get(current_point, 0):.1f}"
        
        self.ax2.text(0.02, 0.98, info_text, transform=self.ax2.transAxes,
                     verticalalignment='top', fontfamily='monospace',
                     bbox=dict(facecolor='white', alpha=0.8))
        
        if show:
            plt.pause(0.001)
    
    def show_final_path(self, path: List[Point]):
        if path:
            path_x = [p.x for p in path]
            path_y = [p.y for p in path]
            self.ax1.plot(path_x, path_y, 'g-', linewidth=3, label='Final Path')
            self.ax1.legend()
        
        plt.show() 