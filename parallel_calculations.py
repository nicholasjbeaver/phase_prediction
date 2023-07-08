import subprocess
import concurrent.futures
import SURP
import argparse

DEBUG_MODE = False

def run_simulation(elements_string):
    if DEBUG_MODE:
        print(f'Running dummy simulation for {elements_string}')
        status = subprocess.run(['python.exe', 'dummy_results.py', f'-e "{elements_string}"', '-d'])
    else:
        print(f'Running simulation for {elements_string}')
        status = subprocess.run(['python.bat', 'SURP.py', f'-e "{elements_string}"'])

    if status.returncode != 0:
        print(f'Error running simulation for {elements_string}')
        return False

    return True


def run_simulation_from_file(filename):
    element_strings = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            element_strings.append(line.strip())

    print(f'Running simulations for {len(element_strings)} elements')

    valid_element_strings = []
    # verify elements in element_strings and remove those that are not supported and log errors for the ones that are not supported
    for element_string in element_strings:
        elements = SURP.extract_elements_from_string(element_string)
        if not SURP.verify_elements(elements):
            print(f'Unsupported elements found in {element_string}')
        else:
            valid_element_strings.append(element_string)

    element_strings = valid_element_strings


    # Use ThreadPoolExecutor to run simulations concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_elements = {executor.submit(run_simulation, element_string): element_string for element_string in
                              element_strings}
        for future in concurrent.futures.as_completed(future_to_elements):
            element_string = future_to_elements[future]
            try:
                success = future.result()
                if success:
                    print(f'Successfully ran simulation for {element_string}')
                else:
                    print(f'Failed to run simulation for {element_string}')
            except Exception as exc:
                print(f'Generated an exception: {exc}')


if __name__ == "__main__":

    # Initialize the parser for input parameters to the this python file
    parser = argparse.ArgumentParser(description="Run a bunch of simulations in parallel")
    parser.add_argument("-i", "--input", help="Input file that contains element strings to run", required=False, default = 'HEA_input.txt')
    # Add a debug flag
    parser.add_argument("-d", "--debug", help="Debug flag", action="store_true", required=False)

    # Parse the arguments, unknown arguments will be ignored...used because running from batch file
    args, unknown = parser.parse_known_args()

    if args.debug == True:
        DEBUG_MODE = True
        print('Debug mode enabled')

    print(f'Running simulations from {args.input}')
    run_simulation_from_file(args.input)
