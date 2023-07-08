import subprocess
import concurrent.futures

from SURP import *


def run_simulation(elements_string):
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

    # verify elements in element_strings and remove those that are not supported
    element_strings = [element_string for element_string in element_strings if SURP.verify_elements(extract_elements_from_string(element_string))]

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
    HEA_INPUT_FILE = 'HEA_input.txt'
    run_simulation_from_file(HEA_INPUT_FILE)
