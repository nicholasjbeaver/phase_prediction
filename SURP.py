import os
import itertools
import argparse
import phase_calculation

def verify_elements(elements):
    # check each element and make sure it is in the supported list
    # if not, return False

    supported_list = ['Hf', 'Nb', 'Ti', 'V', 'Zr']
    for element in elements:
        if element not in supported_list:
            print(f'Unsupported element found {element}')
            return False

    return True


# Create every combination choosing everything from one element up to the length of the list.
# Changing the order of the elements should not be considered a new combination
def create_combinations(elements):
    combinations = []
    for i in range(1, len(elements) + 1):
        combinations.extend(list(itertools.combinations(elements, i)))
    return combinations

def construct_filename_from_elements(elements):
    # sort the elements
    elements.sort()
    filename = ''
    for element in elements:
        filename += element + '_'

    # remove the last underscore and add the extension
    filename = filename[:-1] + '.csv'
    return filename


def construct_filenames_from_combinations(combinations):
    filenames = []
    for combination in combinations:
        filenames.append('_'.join(combination) + '.txt')
    return filenames


# define a function that extracts the elements from the filename
def extract_elements_from_string(element_string):
    elements = element_string.split('.')[0].split('_')
    return elements

def read_status_file(status_file):
    # read in csv file and ignore header row
    # second column is the status and should be converted to a boolean
    # return a list of tuples with the filename and status
    list_of_files = []
    with open(status_file, 'r') as f:
        for line in f.readlines()[1:]:
            filename, status = line.split(',')
            status = status.strip() == "True"
            print(status)
            list_of_files.append((filename, status))

    return list_of_files

def perform_thermo_calculation(output_filename, elements, output_dir = './data' ):
    # perform the thermo calculation
    # return True if successful, False otherwise
    phase_calculation.calculate_phases
    # append the output directory to the filename
    output_filename = os.path.join(output_dir, output_filename)

    # write the header, with Temp, FCC, BCC, HCP, Liquid separated by tabs
    with open(output_filename, 'w') as f:
        f.write('Temp \t FCC \t BCC \t HCP \t Liquid \n')
        for temp in range(1000, 1100, 10):
            f.write(f'{temp} \t1.0\t0.0\t0.0\t0.0\n')

    return True


def write_status_file(status_file, list_of_files):
    # write the list to a file, overwriting the existing file
    # list of files is a list of tuples with the filename and status
    with open(status_file, 'w') as f:
        # write the header
        f.write('Filename, Processed\n')

        for file in list_of_files:
            f.write(f'{file[0]}, {file[1]}\n')

def create_status_list(filenames):
    # create a list of tuples with the filename and status
    # status is False for all files
    status_list = []
    for file in filenames:
        status_list.append((file, False))
    return status_list

if __name__ == '__main__':


    # location where all of the thermo data will be stored
    DATA_DIR = './data'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Initialize the parser for input parameters to the this python file
    parser = argparse.ArgumentParser(description="Takes a list of elements and performs all phase diagrams of combinations.")

    # Add an argument to the parser
    parser.add_argument("-e", "--elements", help="String argument that contains elements separated by _", required=True)
    # Add an optional parameter for an output file
    parser.add_argument("-o", "--output", help="Output file name for status list, optional...will construct name from elements", required=False)
    # Parse the arguments, unknown arguments will be ignored...used because running from batch file
    args, unknown = parser.parse_known_args()

    # Print the arguments
    periodic_elements = extract_elements_from_string(args.elements)
    print("Processing these elements: ", periodic_elements)

    # Verify that the elements are supported
    if not verify_elements(periodic_elements):
        exit(1)

    # Alphabetize the list
    periodic_elements.sort()

    # The status file keeps track of which element combinations have been processed
    # if a status file is provided as a parameter, use it, otherwise construct the name from the elements
    if args.output:
        status_file = args.output
    else:
        status_file = construct_filename_from_elements(periodic_elements)

    # see if the status file exists
    try:
        status_list = read_status_file(status_file)
        print(f'Status file {status_file} found.  Continuing with status file.')
        print(status_list)
    except FileNotFoundError:
        print(f'Status file {status_file} not found.  Creating new status file.')

        # Create a list of all possible combinations of the elements
        combinations = create_combinations(periodic_elements)

        # Print the combinations
        print(f'Number of combos: {len(combinations)}')
        for combination in combinations:
            print(combination)

        filenames = construct_filenames_from_combinations(combinations)
        status_list = create_status_list(filenames)

        # write the status file
        write_status_file(status_file, status_list)

    # loop through the status list and perform the thermo calculation
    for file in status_list:
        if not file[1]:
            print(f'Processing {file[0]}')
            elements = extract_elements_from_string(file[0])
            if perform_thermo_calculation(file[0], elements, output_dir=DATA_DIR):
                # update the status list
                status_list[status_list.index(file)] = (file[0], True)

            # write the status file after each calculation in case of failure, should be able to restart
            write_status_file(status_file, status_list)



