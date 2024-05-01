import math
import random

from sheep import Sheep
from drone import Drone


class World:
    def __init__(self, cell_size: int, cell_number: int):
        self.cell_size = cell_size
        self.cell_number = cell_number
        # First index is x, second is y (grid[x][y])
        self.grid = [[[] for _ in range(cell_number)] for _ in range(cell_number)]

        self.sheep = []
        self.drones = []

    def get_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def add_sheep(self, sheep, x, y):
        cell_x, cell_y = self.get_cell(x, y)
        cell_x = cell_x % self.cell_number
        cell_y = cell_y % self.cell_number
        self.grid[cell_x][cell_y].append(sheep)
        self.sheep.append(sheep)

    def remove_sheep(self, x, y):
        cell_x, cell_y = self.get_cell(x, y)
        cell_x = cell_x % self.cell_number
        cell_y = cell_y % self.cell_number
        cell_content = self.grid[cell_x][cell_y]
        for sheep in cell_content:
            if sheep.x == x and sheep.y == y:
                cell_content.remove(sheep)
                self.sheep.remove(sheep)
                break

    def get_sheep_in_cell(self, cell_x, cell_y):
        return self.grid[cell_x][cell_y]

    def update(self):
        # self.update_sheeps()
        self.updata_drones()

    def update_sheeps(self):
        for sheep in self.sheep:
            sheep.update()

    def updata_drones(self):
        known_targets = []
        for drone in self.drones:
            while True:
                if drone.target_cell is None:
                    drone.find_target()

                    if drone.target_cell not in known_targets:
                        known_targets.append(drone.target_cell)

                        break
                else:
                    break

            drone.move()

        for drone in self.drones:
            drone.calculate_total_force()

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

    def initialize_drones(
        self, num_drones: int, attraction_constant: int, repulsion_constant: int
    ):
        for i in range(num_drones):
            x_cell = random.randint(0, self.cell_number - 1)
            y_cell = random.randint(0, self.cell_number - 1)

            self.drones.append(
                Drone(
                    self,
                    (x_cell, y_cell),
                    i,
                    self.cell_size,
                    self.cell_number,
                    attraction_constant,
                    repulsion_constant,
                )
            )

    @property
    def size(self):
        return self.cell_size * self.cell_number

    @property
    def number_monitored_sheep(self):
        return sum(drone.number_of_sheeps_visible for drone in self.drones)
