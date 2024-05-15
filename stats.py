import argparse
import csv
import os

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

    parser.add_argument("--iteration", type=int, help="The iteration number")

    return parser.parse_args()


def do_test(num_robots, num_sheep, steps, repulsion, attraction, herds_number, iteration):
    args = get_arguments()
    ARENA_SIDE_LENGTH = 300
    CELL_SIZE = 10
    NUMBER_OF_ROBOTS = num_robots
    NUMBER_OF_SHEEP = num_sheep
    STEPS = steps
    ATTRACTION_STRENGTH = - attraction
    REPULSION_STRENGTH = repulsion

    CELL_NUMBER = ARENA_SIDE_LENGTH // CELL_SIZE

    # Create the world object
    world = World(CELL_SIZE, CELL_NUMBER)

    world.initialize_herds(NUMBER_OF_SHEEP, herds_number)
    world.initialize_drones(NUMBER_OF_ROBOTS, ATTRACTION_STRENGTH, REPULSION_STRENGTH)

    monitored_animals = []

    for i in range(STEPS):
        # Update the world
        world.update()

        # If the monitored sheep and the percentage of sheep is the same for 50 steps, and the world has been explored stop the simulation
        limit = 200 
         
        monitored_animals.append(
            (
                world.number_monitored_sheep,
                world.number_monitored_sheep / (NUMBER_OF_SHEEP*herds_number),
                world.world_explored,
            )
        )

        if i > limit and (len(set(monitored_animals[-limit:])) == 1) and world.world_explored:
            break

        # print(f"{i}/{STEPS}")

    # Specify directory path
    directory = "./csv_results_validation/"

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(
        f"{directory}monitored_animals-{NUMBER_OF_ROBOTS}-{ATTRACTION_STRENGTH}-{REPULSION_STRENGTH}-{herds_number}-{iteration}.csv",
        "w",
    ) as f:
        writer = csv.writer(f)
        writer.writerows(monitored_animals)

if __name__ == "__main__":
    args = get_arguments()

    do_test(args.number_of_robots, args.number_of_sheep, args.steps, args.repulsion, args.attraction, args.herds_number, args.interation)