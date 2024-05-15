from multiprocessing import Pool
from stats import do_test

def run_test(params):
    print(f"Running: {params}")
    n_drones, attr, rep, herds, iteration = params
    return do_test(n_drones, 100, 4000, rep, attr, herds, iteration)

if __name__ == "__main__":
    # Define the parameter ranges
    n_drones_range = range(40, 41, 5)
    attr_range = range(340, 361, 20)
    rep_range = range(100, 240, 20)
    iterations = range(0, 15)
    
    # Testing parameters
    # n_drones_range = range(5, 11, 5)
    # attr_range = range(10, 21, 10)
    # rep_range = range(10, 21, 10)
    
    # Generate parameter combinations
    params_list = [(n, a, r, 4, i) for i in iterations for n in n_drones_range for a in attr_range for r in rep_range]
    
    # Initialize a Pool of workers
    with Pool() as pool:
        # Map the do_test function to each parameter combination in parallel
        results = pool.map(run_test, params_list)

    # Process the results as needed
    # For example, you can print or save them
    for result in results:
        # Process each result here
        pass

