import argparse
import time

class Results():

    def __init__(self, x: [], y: [], label: str):
        self.x = x
        self.y = y
        self.label = label

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_label(self):
        return self.label


def x_table(results_dict):
    x_table = {}
    all_x_values = set(x for value in results_dict.values() for x in value.get_x())

    all_x_values = {x for x in all_x_values if isinstance(x, (int, float))}

    for x in all_x_values:
        x_table[x] = {key: None for key in results_dict.keys()}

    for key, value in results_dict.items():
        for x, y in zip(value.get_x(), value.get_y()):
            x_table[x][key] = y

    # order the dictionary by the x values
    x_table = {k: v for k, v in sorted(x_table.items(), key=lambda item: item[0])}
    return x_table


def format_table(x_table, result_dict_keys):
    # add the header
    header = "Temp\t" + "\t".join(result_dict_keys) + "\n"
    table = header

    for x, y in x_table.items():
        row = f"{x}"
        for key in result_dict_keys:
            row += f"\t{y[key]}"
        row += "\n"
        table += row

    return table


def output_txt(table, filename):
    with open(filename, 'w') as f:
        f.write(table)


def create_dummy_results(elements):
    fcc = Results([100, 110, 120], [1, 1, 1], "FCC")
    bcc = Results([130, 140, 150], [1, 1, 1], "BCC")

    calc_results = {"FCC": fcc, "BCC": bcc}
    return calc_results


if __name__ == "__main__":

   # Initialize the parser for input parameters to the this python file
    parser = argparse.ArgumentParser(description="Takes a list of elements and performs all phase diagrams of combinations.")

    # Add an argument to the parser
    parser.add_argument("-e", "--elements", help="String argument that contains elements separated by _", required=False, default="Al_Cu")
    # Add an optional parameter for an output file
    parser.add_argument("-o", "--output", help="Output file name for status list, optional...will construct name from elements", required=False)
    # Add a debug flag
    parser.add_argument("-d", "--debug", help="Debug flag", action="store_true", required=False)

    # Parse the arguments, unknown arguments will be ignored...used because running from batch file
    args, unknown = parser.parse_known_args()

    calc_results = create_dummy_results(args.elements)
    x_table_result = x_table(calc_results)

    print(x_table_result)
    print(format_table(x_table_result, calc_results.keys()))

    if args.debug:
        # waste some time
        print(f'Simulating doing stuff with these elements: {args.elements}')
        # sleep for 10 seconds
        time.sleep(10)
        print("Done simulating...")

    exit(0)

