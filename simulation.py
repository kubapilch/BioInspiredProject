import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from world import World

plt.rcParams["animation.ffmpeg_path"] = r"C:\ffmpeg\bin\ffmpeg.exe"

ARENA_SIDE_LENGTH = 100
CELL_SIZE = 10
CELL_NUMBER = ARENA_SIDE_LENGTH // CELL_SIZE
NUMBER_OF_ROBOTS = 10
NUMBER_OF_SHEEP = 50
STEPS = 500

# Create the world object
world = World(CELL_SIZE, CELL_NUMBER)

world.initialize_herd(NUMBER_OF_SHEEP)
world.initialize_drones(NUMBER_OF_ROBOTS)

# Set up the output (1024 x 768):
fig = plt.figure(figsize=(10.24, 7.68), dpi=100)
ax = plt.axes(xlim=(0, ARENA_SIDE_LENGTH), ylim=(0, ARENA_SIDE_LENGTH))

(drone_points,) = ax.plot([], [], "bo", lw=0, label="Drone")
(sheep_points,) = ax.plot([], [], "ro", lw=0, label="Sheep")
direction_lines = [ax.plot([], [], "k-", lw=1)[0] for _ in range(NUMBER_OF_ROBOTS)]  # Lines indicating direction
drone_labels = [ax.text(0, 0, "", ha='center', va='center') for _ in range(NUMBER_OF_ROBOTS)]  # Labels for drones

ax.legend()

def init():
    drone_points.set_data([], [])
    sheep_points.set_data([], [])
    return drone_points, sheep_points

def plot_visibility_squares():
     for drone in world.drones:
        x, y = drone.absolute_pos
        ax.add_patch(plt.Rectangle((x - CELL_SIZE/2, y - CELL_SIZE/2), CELL_SIZE, CELL_SIZE, color='b', alpha=0.1))

def plot_visited_cells():
    plotted_cells = []

    for drone in world.drones:
        for x in range(world.cell_number):
            for y in range(world.cell_number):
                if drone.visited_cells[x][y] and not (x, y) in plotted_cells:
                    ax.add_patch(plt.Rectangle((x * CELL_SIZE, y * CELL_SIZE), CELL_SIZE, CELL_SIZE, color='r', alpha=0.1))

                    plotted_cells.append((x, y))

    

def plot_direction_lines():
    for i, drone in enumerate(world.drones):
        if drone.target_cell:
            # Calculate the center of the target cell
            target_x = drone.target_cell[0] * CELL_SIZE + CELL_SIZE / 2
            target_y = drone.target_cell[1] * CELL_SIZE + CELL_SIZE / 2
            # Update line between drone and center of target cell
            direction_lines[i].set_data([drone.absolute_pos[0], target_x], [drone.absolute_pos[1], target_y])

def plot_drone_labels():
    for i, drone in enumerate(world.drones):
        # Update drone label
        drone_labels[i].set_text(f"Sheep: {drone.number_of_sheeps_visible}")
        drone_labels[i].set_position((drone.absolute_pos[0], drone.absolute_pos[1] + CELL_SIZE))

def animate(i):
    if(i % 10 != 0):
        return drone_points, sheep_points
    
    # Update the world
    world.update()

    # Update drone positions on the plot
    positions_x = [world.drones[i].absolute_pos[0] for i in range(NUMBER_OF_ROBOTS)]
    positions_y = [world.drones[i].absolute_pos[1] for i in range(NUMBER_OF_ROBOTS)]

    drone_points.set_data(positions_x, positions_y)

    # Remove overlays
    for overlay in ax.patches:
        overlay.remove()

    plot_visibility_squares()  # Plot new circles
    plot_visited_cells() # Plot visited cells¨
    plot_direction_lines()  # Plot direction lines
    plot_drone_labels()  # Plot drone labels

    # Update sheep positions on the plot
    sheep_positions_x = [sheep.x for sheep in world.sheep]
    sheep_positions_y = [sheep.y for sheep in world.sheep]
    sheep_points.set_data(sheep_positions_x, sheep_positions_y)

    print("Step ", i + 1, "/", STEPS, end="\r")

    return drone_points, sheep_points


anim = FuncAnimation(fig, animate, init_func=init, frames=STEPS, interval=1, blit=True)

plt.show()
videowriter = animation.FFMpegWriter(fps=10)
anim.save("output.mp4", writer=videowriter)
