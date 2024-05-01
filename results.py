from multiprocessing import Pool
from stats import do_test

def run_test(params):
    print(f"Running: {params}")
    n_drones, attr, rep, herds = params
    return do_test(n_drones, 40, 2000, rep, attr, herds)

if __name__ == "__main__":
    # Define the parameter ranges
    n_drones_range = range(5, 51, 5)
    attr_range = range(10, 501, 10)
    rep_range = range(10, 501, 10)
    
    # Testing parameters
    # n_drones_range = range(5, 11, 5)
    # attr_range = range(10, 21, 10)
    # rep_range = range(10, 21, 10)
    
    # Generate parameter combinations
    params_list = [(n, a, r, 3) for n in n_drones_range for a in attr_range for r in rep_range]
    
    # Initialize a Pool of workers
    with Pool(3) as pool:
        # Map the do_test function to each parameter combination in parallel
        results = pool.map(run_test, params_list)

    # Process the results as needed
    # For example, you can print or save them
    for result in results:
        # Process each result here
        pass

