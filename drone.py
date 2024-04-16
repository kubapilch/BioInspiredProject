import random

class Drone:
    
    speed = 0.1
    arena_size = 100
    velocity = (1, 1)

    def __init__(self, pos:tuple, arena_size:int=100):
        self.pos = pos
        self.arena_size = arena_size

    def update_velocity(self):
        self.velocity = (self.speed * (2 * random.random() - 1), self.speed * (2 * random.random() - 1))

        # if the drone is going out of the arena, invert the velocity
        if self.pos[0] < 0 or self.pos[0] > self.arena_size:
            self.velocity = (-self.velocity[0], self.velocity[1])


    def move(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])

        self.update_velocity()
