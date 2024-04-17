import math
import random

from sheep import Sheep
from drone import Drone

class World:
    def __init__(self, cell_size:int, cell_number:int):
        self.cell_size = cell_size
        self.cell_number = cell_number
        # First index is x, second is y (grid[x][y])
        self.grid = [[[] for _ in range(cell_number)] for _ in range(cell_number)]
        
        self.sheep = []
        self.drones = []

    def get_cell(self, x:int, y:int):
        return x // self.cell_size, y // self.cell_size

    def add_sheep(self, sheep:Sheep, x:int, y:int):
        cell_x, cell_y = self.get_cell(x, y)
        
        self.grid[cell_x][cell_y].append(sheep)
        self.sheep.append(sheep)

    def get_sheep_in_cell(self, cell_x, cell_y):
        return self.grid[cell_x][cell_y]

    def update(self):
        self.update_sheeps()
        self.updata_drones()

    def update_sheeps(self):
        for sheep in self.sheep:
            sheep.update()
    
    def updata_drones(self):
        for drone in self.drones:
            if drone.target_cell is None:
                drone.find_target()

            drone.move()

    def initialize_herd(self, num_sheep):
        # Calculate initial spawn area radius
        radius = math.sqrt(num_sheep)
        center_x = self.size // 2
        center_y = self.size // 2

        for _ in range(num_sheep):
            # Generate random positions within the circle
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0, radius)
            x = int(center_x + dist * math.cos(angle))
            y = int(center_y + dist * math.sin(angle))

            # Ensure position is within world bounds
            x = (x + self.size) % self.size  # handle negative or out-of-bounds values
            y = (y + self.size) % self.size

            # Add sheep to the world
            self.add_sheep(Sheep(self, x, y), x, y)

    def initialize_drones(self, num_drones):
        for i in range(num_drones):
            x_cell = random.randint(0, self.cell_number - 1)
            y_cell = random.randint(0, self.cell_number - 1)
            
            self.drones.append(Drone(self, (x_cell, y_cell), i, self.cell_size, self.cell_number))

    @property
    def size(self):
        return self.cell_size * self.cell_number
    