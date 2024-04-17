import random
from math import pi

class Message:
    def __init__(
        self,
        sender_id: int,
        message_id: int,
        current_cell: tuple,
        number_of_sheeps: int,
        target_cell: tuple,
    ):
        self.sender_id = sender_id
        self.message_id = message_id
        self.current_cell = current_cell
        self.number_of_sheeps = number_of_sheeps
        self.target_cell = target_cell


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

        self.taking_picture = False

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

            return
        elif self.cell_pos == self.target_cell:
            self.taking_picture = True

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

    def find_target(self):
        """
        Find the target cell for the drone to move to
        """
        # momentum vector
        m = (0, 0)
        # repulsion vector
        r = (0, 0)
        # attraction vector
        a = (0, 0)

        possible_cells = []

        # Make the set of valid cells, based on the direction of the resulting vector and the distance to the cell from the current position
        # Loop through cells which are 1 coordinate away from the current cell
        for i in range(1, self.cell_number):
            if (
                self.cell_pos[0] + i < self.cell_number
                and not self.visited_cells[self.cell_pos[0] + i][self.cell_pos[1]]
            ):
                possible_cells.append((self.cell_pos[0] + i, self.cell_pos[1]))

            if (
                self.cell_pos[0] - i >= 0
                and not self.visited_cells[self.cell_pos[0] - i][self.cell_pos[1]]
            ):
                possible_cells.append((self.cell_pos[0] - i, self.cell_pos[1]))

            if (
                self.cell_pos[1] + i < self.cell_number
                and not self.visited_cells[self.cell_pos[0]][self.cell_pos[1] + i]
            ):
                possible_cells.append((self.cell_pos[0], self.cell_pos[1] + i))

            if (
                self.cell_pos[1] - i >= 0
                and not self.visited_cells[self.cell_pos[0]][self.cell_pos[1] - i]
            ):
                possible_cells.append((self.cell_pos[0], self.cell_pos[1] - i))
  
            # If there are possible cells to move to, break the loop
            if len(possible_cells) != 0:
                break
        else:
            # No cells found
            return

        self.target_cell = random.choice(possible_cells)
        self.send_message()

        self.visited_cells[self.target_cell[0]][self.target_cell[1]] = True

    def send_message(self):
        self.message_count += 1
        message = Message(
            self.id,
            self.message_count,
            self.cell_pos,
            self.number_of_sheeps_visible,
            self.target_cell,
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

            self.forward_message(message)

    @property
    def absolute_pos(self):
        return (
            (self.cell_pos[0] * self.cell_size) + self.cell_size / 2,
            (self.cell_pos[1] * self.cell_size) + self.cell_size / 2,
        )

    @staticmethod
    def cauchy(theta, p):
        return 1/(2*pi)
