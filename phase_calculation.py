from tc_python import *

elements=['Hf', 'Nb']

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
		if len(elements) !=1:
			for element in elements[0:-1]:
				prop_diag.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element), 1/len(elements))		 

		# calculate
		calculation = prop_diag.calculate()

		# get values grouped by stable phases
		property_diagram = calculation.get_values_grouped_by_stable_phases_of(ThermodynamicQuantity.temperature(), ThermodynamicQuantity.volume_fraction_of_a_phase("ALL"))

		property_diagram.save_to_disk('C:\code\github')
	# get result quantities
		

calculate_phases(elements)


