import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from drone import Drone
from herd_sim import Sheep, World,initialize_herd, update_herd

plt.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'

ARENA_SIDE_LENGTH = 50

NUMBER_OF_ROBOTS  = 1
NUMBER_OF_SHEEP   = 50
STEPS             = 1000
MAX_SPEED         = 0.1
INTERVAL          =1

# Create the world object
world = World(ARENA_SIDE_LENGTH, 4,INTERVAL)

# Initialize the sheep herd
initialize_herd(world, NUMBER_OF_SHEEP)
# Positions

#x = np.random.uniform(low=0, high=ARENA_SIDE_LENGTH, size=(NUMBER_OF_ROBOTS,))
#y = np.random.uniform(low=0, high=ARENA_SIDE_LENGTH, size=(NUMBER_OF_ROBOTS,))

# Velocities
#vx = np.random.uniform(low=-MAX_SPEED, high=MAX_SPEED, size=(NUMBER_OF_ROBOTS,))
#vy = np.random.uniform(low=-MAX_SPEED, high=MAX_SPEED, size=(NUMBER_OF_ROBOTS,))

# Set up the output (1024 x 768):
fig = plt.figure(figsize=(10.24, 7.68), dpi=100)
ax = plt.axes(xlim=(0, ARENA_SIDE_LENGTH), ylim=(0, ARENA_SIDE_LENGTH))
points, = ax.plot([], [], 'bo', lw=0, )


drones = [Drone((x[i], y[i])) for i in range(NUMBER_OF_ROBOTS)]

# Make the environment toroidal 
def wrap(z):    
    return z % ARENA_SIDE_LENGTH

def init():
    points.set_data([], [])
    return points,

def animate(i):    
    for drone in drones:
        drone.move()
    
    positions_x = [drones[i].pos[0] for i in range(NUMBER_OF_ROBOTS)]
    positions_y = [drones[i].pos[1] for i in range(NUMBER_OF_ROBOTS)]
    
    points.set_data(positions_x, positions_y)

    points.set_data(update_herd(world))

    print('Step ', i + 1, '/', STEPS, end='\r')

    return points,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=STEPS, interval=1, blit=True)
plt.show()
videowriter = animation.FFMpegWriter(fps=60)
anim.save("output.mp4", writer=videowriter)