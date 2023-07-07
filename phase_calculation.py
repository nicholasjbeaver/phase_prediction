from tc_python import *
import os
import itertools
elements=['Hf','Zr']

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
	
def format_results(property_diagram):
	
	temperature=[]

	for key,value in property_diagram.items():
		x_values = value.get_x()
		for x in x_values:
			



	property_diagram
	with open('output.txt', 'w') as f:
		f.write('Key\tValue_X\tValue_Y\n')
		for key, value in property_diagram.items():
			x_values = value.get_x()
			y_values = value.get_y()
			for x, y in itertools.zip_longest(x_values, y_values):
				f.write(f'{key}\t{x}\t{y}\n')


result = calculate_phases(elements)
format_results(result)

