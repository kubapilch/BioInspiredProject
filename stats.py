import argparse
import csv

from world import World

def get_arguments():
    parser = argparse.ArgumentParser(description="Run the simulation")

    parser.add_argument(
        "--number_of_robots",
        type=int,
        help="The number of robots",
    )
    parser.add_argument(
        "--number_of_sheep",
        type=int,
        help="The number of sheep",
    )
    parser.add_argument("--steps", type=int, default=2000, help="The number of steps to simulate")

    parser.add_argument("--repulsion", type=int, help="The repulsion strength of the drones")
    
    parser.add_argument(
        "--attraction", type=int, help="The attraction strength of the beacons")
    

    return parser.parse_args()


if __name__ == "__main__":

    args = get_arguments()
    ARENA_SIDE_LENGTH = args.arena_side_length
    CELL_SIZE = args.cell_size
    NUMBER_OF_ROBOTS = args.number_of_robots
    NUMBER_OF_SHEEP = args.number_of_sheep
    STEPS = args.steps
    ATTRACTION_STRENGTH = args.attraction
    REPULSION_STRENGTH = args.repulsion

    CELL_NUMBER = ARENA_SIDE_LENGTH // CELL_SIZE

    REPULSION_CONSTANT = 125
    ATTRACTION_CONSTANT = -200

    # Create the world object
    world = World(CELL_SIZE, CELL_NUMBER)

    world.initialize_herd(NUMBER_OF_SHEEP)
    world.initialize_drones(NUMBER_OF_ROBOTS)

    monitored_animals = []

    for i in range(STEPS):
        # Update the world
        world.update()

        monitored_animals.append(
            [
                world.number_monitored_sheep,
                world.number_monitored_sheep / NUMBER_OF_SHEEP,
            ]
        )

    with open(f"monitored_animals-{NUMBER_OF_ROBOTS}-{ATTRACTION_STRENGTH}-{REPULSION_STRENGTH}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(monitored_animals)


