from tc_python import *
import os
import itertools
import numpy as np


def calculate_phases(elements):
	with TCPython() as start:
		# select database and elements
		db_elements = start.select_database_and_elements("TCHEA4", elements)

		# get system
		system = db_elements.get_system()

		# set property diagram calculation
		prop_diag_calc = system.with_property_diagram_calculation()

		# set axis
		axis = CalculationAxis(ThermodynamicQuantity.temperature()).set_min(100).set_max(2500)
		prop_diag = prop_diag_calc.with_axis(axis)

		# set conditions
		if len(elements) > 1:
			for element in elements[0:-1]:
				prop_diag.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element), 1/len(elements))		 

		# calculate
		calculation = prop_diag.calculate()

		# get values grouped by stable phases
		property_diagram = calculation.get_values_grouped_by_quantity_of(ThermodynamicQuantity.temperature(), ThermodynamicQuantity.mole_fraction_of_a_phase("ALL"), sort_and_merge=False)

		return property_diagram

		
	# get result quantities
def x_table(results_dict):
    x_table = {}
    all_x_values = set(x for value in results_dict.values() for x in value.get_x())

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

if __name__ =='__main__':
	elements=['Hf','Zr']
	result = calculate_phases(elements)
	table = x_table(result)
	formatted = format_table(table, result.keys())
	output_txt(formatted, 'output.txt')

