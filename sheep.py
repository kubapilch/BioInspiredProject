import math
import random
import numpy as np
import random
from scipy.spatial import ConvexHull

class Sheep:
    def __init__(self, world, x, y, state="idle"):
        self.world = world
        self.x = x
        self.y = y
        self.state = state
        self.speed = 0  # adjust speed as needed
        self.orientation = random.uniform(-math.pi, math.pi)
        self.desired_speed = 0
        self.desired_orientation = random.uniform(-math.pi, math.pi)

    def get_neighbors(self):
        cell_number = self.world.cell_number
        cell_x, cell_y = self.world.get_cell(self.x, self.y)
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_x = (cell_x + dx) % cell_number
                neighbor_y = (cell_y + dy) % cell_number
                neighbors.extend(self.world.get_sheep_in_cell(neighbor_x, neighbor_y))
        if self in neighbors:
            neighbors.remove(self)

        return neighbors

    def get_alignment_influence(self, neighbors):
        if not neighbors:
            return 0  # No neighbors, no influence
        average_direction = sum(neighbor.orientation for neighbor in neighbors) / len(
            neighbors
        )
        return average_direction

    def get_separation_force(self, neighbors, sheep_radius):
        repulsive_force = (0, 0)
        repulsive_dir = 0
        for neighbor in neighbors:
            distance = math.sqrt(
                ((self.x - neighbor.x) % self.world.size) ** 2
                + ((self.y - neighbor.y) % self.world.size) ** 2
            )
            if distance < sheep_radius and distance != 0:
                # Calculate unit vector pointing away from neighbor
                repulsion_direction = (self.x - neighbor.x, self.y - neighbor.y)
                repulsive_force += (
                    repulsion_direction[0] / distance,
                    repulsion_direction[1] / distance,
                )  # direction and magnitude
                repulsive_dir += math.atan2(
                    repulsive_force[1], repulsive_force[0]
                )  # solely direction
        return repulsive_dir / (len(neighbors) or 1)

    def get_fence_repulsion(self, fence_repulsion_factor):
        """Calculates a repulsive force vector based on distance to fences"""
        distance_to_fence = min(
            abs(self.x - self.world.size), abs(self.y - self.world.size)
        )
        repulsion_strength = fence_repulsion_factor * (
            1 - distance_to_fence / self.world.size
        )
        dir = self.orientation + math.pi
        return dir, repulsion_strength

    def update_orienation(self):
        rand_angle = random.uniform(-math.pi, math.pi)
        neighbors = self.get_neighbors()
        average_orienation = self.get_alignment_influence(neighbors)
        repulsive_dir = self.get_separation_force(neighbors, 1)
        fence_repulsion, fence_r_factor = self.get_fence_repulsion(1)  # 0.1
        inv_repulsive_dir = repulsive_dir + math.pi

        if self.state == "walking":
            total_influence = (fence_repulsion * fence_r_factor+ 1- fence_r_factor* ((inv_repulsive_dir * 0.9 + average_orienation * 0.1) / 2)) / 2 + rand_angle
        else:
            _, c = self.get_herd_hull_area()
            total_influence = math.atan2(abs(self.y - c[1]), abs(self.x - c[0]))
        return total_influence

    def get_herd_hull_area(self):
        # Identify cells with sheep
        occupied_cells = []
        for cell_x in range(self.world.cell_number):
            for cell_y in range(self.world.cell_number):
                if self.world.get_sheep_in_cell(cell_x, cell_y):
                    occupied_cells.append((cell_x, cell_y))

        # Extract sheep positions
        sheep_positions = []
        for cell_x, cell_y in occupied_cells:
            world_x = cell_x * self.world.cell_number + self.world.cell_number // 2
            world_y = cell_y * self.world.cell_number + self.world.cell_number // 2
            sheep_positions.append((world_x, world_y))

        # Calculate convex hull area (if needed)
        if len(sheep_positions) < 2:
            return 0, [0, 0]
        
        hull = ConvexHull(sheep_positions)
        c = []
        for i in range(hull.points.shape[1]):
            c.append(np.mean(hull.points[hull.vertices, i]))
        return hull.area, c

    def update(self):
        # Update state based on neighbors and environment
        neighbors = self.get_neighbors()
        idle_neighbors = len([n for n in neighbors if n.state == "idle"])
        # print(f"idle {idle_neighbors}")
        running_neighbors = len([n for n in neighbors if n.state == "running"])
        # print(f"running {running_neighbors}")
        walking_neighbors = len([n for n in neighbors if n.state == "walking"])
        # print(f"walking {walking_neighbors}")
        idle_to_walk_coef = 24
        walk_to_idle_coef = 8
        running_threshold = 14
        stopping_mimicking_factor = 0.5
        running_mimicking_factor = 2
        mimicking_factor = 15
        rand = random.random()
        hull_area, hull_center = self.get_herd_hull_area()
        if self.state == "idle":
            # idle to walking
            p = (1 + mimicking_factor * walking_neighbors) / idle_to_walk_coef
            switch_p = 1 - math.exp(-p)
            if rand > switch_p:
                self.state = "walking"
            # idle to running

            p = math.exp((hull_area - running_threshold)) * (
                1 + running_mimicking_factor * (running_neighbors)
            )

            switch_p = 1 - math.exp(-p)
            if rand > switch_p:
                self.state = "running"

        elif self.state == "walking":
            self.desired_speed = 1
            self.desired_orientation = self.update_orienation()
            # walking to idle
            p = (1 + mimicking_factor * idle_neighbors) / walk_to_idle_coef
            switch_p = 1 - math.exp(-p)
            if rand > switch_p:
                self.state = "idle"
            # walking to running
            p = (1 + running_mimicking_factor * (running_neighbors)) * math.exp(
                hull_area - running_threshold
            )
            switch_p = 1 - math.exp(-p)
            if rand > switch_p:
                self.state = "running"

        elif self.state == "running":
            self.desired_speed = 10
            self.desired_orientation = self.update_orienation()
            d = math.sqrt(
                ((self.x - hull_center[0]) % self.world.size) ** 2
                + ((self.y - hull_center[1]) % self.world.size) ** 2
            )
            p = (
                1
                / (math.exp(d) - 0.8)
                * (1 + stopping_mimicking_factor * idle_neighbors)
            )
            switch_p = 1 - math.exp(-p)
            if rand > switch_p:
                self.state = "idle"

        # Move sheep based on state
        if self.state != "idle":
            self.world.remove_sheep(self.x,self.y)
            new_x, new_y = self.move()
            self.x = new_x
            self.y = new_y
            self.world.add_sheep(self,self.x,self.y)

    def move(self):

        max_speed_change = 0.2
        max_dir_change = 0.5
        deltaT = 1
        world_size = self.world.size
        speed_ex = min(
            max((self.desired_speed - self.speed), -(max_speed_change * deltaT)),
            (max_speed_change * deltaT),
        )
        self.speed = self.speed + deltaT * speed_ex
        orientation_ex = min(
            max(
                (self.desired_orientation - self.orientation),
                -(max_dir_change * deltaT),
            ),
            (max_dir_change * deltaT),
        )
        self.orientation = self.orientation + deltaT * orientation_ex
        speed_y = self.speed * math.sin(self.orientation)
        speed_x = self.speed * math.cos(self.orientation)
        new_x = (self.x + deltaT * speed_x) % world_size
        new_y = (self.y + deltaT * speed_y) % world_size
        return new_x, new_y
