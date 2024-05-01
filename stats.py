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
    parser.add_argument(
        "--steps", type=int, default=2000, help="The number of steps to simulate"
    )

    parser.add_argument(
        "--repulsion", type=int, help="The repulsion strength of the drones"
    )

    parser.add_argument(
        "--attraction", type=int, help="The attraction strength of the beacons"
    )

    parser.add_argument("--herds_number", type=int, help="The number of herds")

    return parser.parse_args()


if __name__ == "__main__":

    args = get_arguments()
    ARENA_SIDE_LENGTH = 200
    CELL_SIZE = 10
    NUMBER_OF_ROBOTS = args.number_of_robots
    NUMBER_OF_SHEEP = args.number_of_sheep
    STEPS = args.steps
    ATTRACTION_STRENGTH = - args.attraction
    REPULSION_STRENGTH = args.repulsion

    CELL_NUMBER = ARENA_SIDE_LENGTH // CELL_SIZE

    # Create the world object
    world = World(CELL_SIZE, CELL_NUMBER)

    world.initialize_herds(NUMBER_OF_SHEEP, args.herds_number)
    world.initialize_drones(NUMBER_OF_ROBOTS, ATTRACTION_STRENGTH, REPULSION_STRENGTH)

    monitored_animals = []

    for i in range(STEPS):
        # Update the world
        world.update()

        monitored_animals.append(
            [
                world.number_monitored_sheep,
                world.number_monitored_sheep / NUMBER_OF_SHEEP,
                world.world_explored,
            ]
        )

        print(f"{i}/{STEPS}")

    with open(
        f"monitored_animals-{NUMBER_OF_ROBOTS}-{ATTRACTION_STRENGTH}-{REPULSION_STRENGTH}-{args.herds_number}.csv",
        "w",
    ) as f:
        writer = csv.writer(f)
        writer.writerows(monitored_animals)
