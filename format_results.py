
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


if __name__ == "__main__":
    fcc = Results([100, 110, 120], [1, 1, 1], "FCC")
    bcc = Results([130, 140, 150], [1, 1, 1], "BCC")

    calc_results = {"FCC": fcc, "BCC": bcc}

    x_table_result = x_table(calc_results)

    print(x_table_result)

    print(format_table(x_table_result, calc_results.keys()))
