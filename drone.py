import random
import math
import cmath
import numpy as np

REPULSION_CONSTANT = 125
ATTRACTION_CONSTANT = -200


class Message:
    def __init__(
        self,
        sender_id: int,
        message_id: int,
        current_cell: tuple,
        number_of_sheeps: int,
        target_cell: tuple,
        beacons: list,
    ):
        self.sender_id = sender_id
        self.message_id = message_id
        self.current_cell = current_cell
        self.number_of_sheeps = number_of_sheeps
        self.target_cell = target_cell
        self.beacons = beacons


class Beacon:
    def __init__(self, cell_pos, cell_size, strength, start_time):
        self.cell_size = cell_size
        self.cell_pos = cell_pos
        self.strength = strength
        self.start_time = start_time

    @property
    def absolute_pos(self):
        return (
            (self.cell_pos[0] * self.cell_size) + self.cell_size / 2,
            (self.cell_pos[1] * self.cell_size) + self.cell_size / 2,
        )


class Drone:

    def __init__(
        self, world, cell_pos: tuple, id: int, cell_size: int, cell_number: int
    ):
        self.cell_pos = cell_pos
        self.cell_size = cell_size
        self.cell_number = cell_number

        self.id = id

        self.number_of_sheeps_visible = 0

        self.received_messages = []
        self.message_count = 0

        self.world = world
        self.radio_range = 10

        self.visited_cells = [
            [False for _ in range(cell_number)] for _ in range(cell_number)
        ]
        self.target_cell = None
        self.fully_explored = False

        self.taking_picture = False

        # momentum vector
        self.momentum = [0, 0]
        self.repulsion = [0, 0]
        # attraction vector
        self.attraction = [0, 0]
        self.beacons = []

        self.total_vector = [0, 0]

        self.ATTRACTION_SPREAD = 32
        self.REPULSION_SPREAD = 64

    def investigate_cell(self):
        self.number_of_sheeps_visible = len(
            self.world.get_sheep_in_cell(*self.cell_pos)
        )

        if self.number_of_sheeps_visible > 0:
            for b in self.beacons:
                if b.cell_pos == self.cell_pos:
                    return

            self.beacons.append(
                Beacon(self.cell_pos, self.cell_size, self.number_of_sheeps_visible, 0)
            )

            self.send_message()

    def move(self):
        """
        Move the drone in the direction of the target cell
        """
        # If no target cell do not move
        if self.target_cell is None:
            return

        # If target reached, clear target and return
        if self.cell_pos == self.target_cell and self.taking_picture:
            self.target_cell = None
            self.taking_picture = False

            return
        elif self.cell_pos == self.target_cell:
            self.taking_picture = True
            self.investigate_cell()

            return

        # Move X
        if self.cell_pos[0] < self.target_cell[0]:
            self.cell_pos = (self.cell_pos[0] + 1, self.cell_pos[1])

        elif self.cell_pos[0] > self.target_cell[0]:
            self.cell_pos = (self.cell_pos[0] - 1, self.cell_pos[1])

        # Move Y
        if self.cell_pos[1] < self.target_cell[1]:
            self.cell_pos = (self.cell_pos[0], self.cell_pos[1] + 1)

        elif self.cell_pos[1] > self.target_cell[1]:
            self.cell_pos = (self.cell_pos[0], self.cell_pos[1] - 1)

        self.send_message()

    @staticmethod
    def generate_squares(input_value):
        if input_value == 0:
            return [(0, 0)]
        result = []
        for i in range(-input_value, input_value + 1):
            result.append((-input_value, i))
            result.append((input_value, i))
            result.append((i, -input_value))
            result.append((i, input_value))

        return set(result)

    def find_target(self):
        """
        Find the target cell for the drone to move to
        """
        possible_cells = []

        x_pos = self.absolute_pos[0] + self.total_vector[0]
        y_pos = self.absolute_pos[1] + self.total_vector[1]

        if x_pos < 0:
            x_pos = 1
        elif x_pos > self.cell_number * self.cell_size:
            x_pos = self.cell_number * self.cell_size - 1

        if y_pos < 0:
            y_pos = 1
        elif y_pos > self.cell_number * self.cell_size:
            y_pos = self.cell_number * self.cell_size - 1

        starting_cell = self.world.get_cell(x_pos, y_pos)

        if self.number_of_sheeps_visible > 0 and self.fully_explored:
            self.target_cell = self.cell_pos
            self.send_message()

            return
        
        # Make the set of valid cells, based on the direction of the resulting vector and the distance to the cell from the current position
        # Loop through cells which are 1 coordinate away from the current cell
        for i in range(0, self.cell_number):

            cells_to_check = self.generate_squares(i)
            for cell in cells_to_check:

                if starting_cell[0] + cell[0] >= self.cell_number:
                    continue

                if starting_cell[0] + cell[0] < 0:
                    continue

                if starting_cell[1] + cell[1] >= self.cell_number:
                    continue

                if starting_cell[1] + cell[1] < 0:
                    continue

                if (
                    self.visited_cells[starting_cell[0] + cell[0]][
                        starting_cell[1] + cell[1]
                    ]
                    and not self.fully_explored
                ):
                    continue

                possible_cells.append((starting_cell[0] + cell[0], starting_cell[1] + cell[1]))

            # If there are possible cells to move to, break the loop
            if len(possible_cells) != 0:
                break
        else:
            # Check if all cells are visited
            if not self.fully_explored and all([all(x) for x in self.visited_cells]):
                self.fully_explored = True

            # No cells found
            return

        # Choose a random cell from the possible cells
        self.target_cell = random.choice(possible_cells)
        self.send_message()

        # Mark the cell as visited
        self.visited_cells[self.target_cell[0]][self.target_cell[1]] = True

    def send_message(self):
        self.message_count += 1
        message = Message(
            self.id,
            self.message_count,
            self.cell_pos,
            self.number_of_sheeps_visible,
            self.target_cell,
            self.beacons,
        )

        for neighbor in self.world.drones:
            if neighbor.id == self.id:
                continue

            if self.get_distance(neighbor) <= self.radio_range:
                neighbor.receive_message(message)

        return message

    def forward_message(self, message: Message):
        for neighbor in self.world.drones:
            if neighbor.id == self.id:
                continue

            if self.get_distance(neighbor) <= self.radio_range:
                neighbor.receive_message(message)

    def get_distance(self, drone):
        return (
            (self.cell_pos[0] - drone.cell_pos[0]) ** 2
            + (self.cell_pos[1] - drone.cell_pos[1]) ** 2
        ) ** 0.5

    def receive_message(self, message: Message):
        if f"{message.sender_id}-{message.message_id}" not in self.received_messages:
            self.received_messages.append(f"{message.sender_id}-{message.message_id}")

            self.visited_cells[message.target_cell[0]][message.target_cell[1]] = True

            for b in message.beacons:
                if b.cell_pos not in [beacon.cell_pos for beacon in self.beacons]:
                    self.beacons.append(b)

            self.forward_message(message)

    @property
    def absolute_pos(self):
        return (
            (self.cell_pos[0] * self.cell_size) + self.cell_size / 2,
            (self.cell_pos[1] * self.cell_size) + self.cell_size / 2,
        )

    @staticmethod
    def cauchy(theta, p):
        return 1 / (2 * math.pi)

    @staticmethod
    def gaussian_vector(v: list, spread: float):
        v = np.array(v)
        length = np.linalg.norm(v)
        v_angle = math.atan2(v[1], v[0])
        a = cmath.exp(1j * v_angle)
        b = cmath.exp(-length / (2 * spread**2))
        return 2 * a * b

    @staticmethod
    def electric_repulsion(r, constant: float):
        force = np.zeros(2)

        r = np.array(r)

        if np.linalg.norm(r) == 0:
            return force

        force = constant * r / np.linalg.norm(r) ** 2

        return force

    def calculate_repulsion_forces(self):
        # Calculate repulsion vector

        sum = [0, 0]
        for drone in self.world.drones:
            if drone.id == self.id:
                continue

            distance = [
                self.absolute_pos[0] - drone.absolute_pos[0],
                self.absolute_pos[1] - drone.absolute_pos[1],
            ]

            res = self.electric_repulsion(distance, REPULSION_CONSTANT)

            np.add(np.random.normal(0, self.REPULSION_SPREAD, size=2), res)

            sum[0] += res[0]
            sum[1] += res[1]

        self.repulsion = sum

    def calculate_attraction_forces(self):
        sum = [0, 0]
        for beacon in self.beacons:
            distance = [
                self.absolute_pos[0] - beacon.absolute_pos[0],
                self.absolute_pos[1] - beacon.absolute_pos[1],
            ]

            res = self.electric_repulsion(distance, ATTRACTION_CONSTANT)

            # increase the attraction force by the beacon strength
            # res[0] *= (res[0] * beacon.strength * 0.1)
            # res[1] *= (res[1] * beacon.strength * 0.1)

            # add randomness
            # np.add(np.random.normal(0, self.ATTRACTION_SPREAD, size=2), res)

            sum[0] += res[0]
            sum[1] += res[1]

        self.attraction = sum

    def calculate_total_force(self):
        self.calculate_repulsion_forces()
        self.calculate_attraction_forces()

        np_total = np.array(self.repulsion) + np.array(self.attraction)

        self.total_vector = np_total.tolist()
