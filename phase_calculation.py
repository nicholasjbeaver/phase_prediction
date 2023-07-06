from tc_python import *


with TCPython() as start:
	gibbs_energy = (
		system = start.select_database_and_elements("TCHEA4", ["Fe", "Cr", "C"]).get_system().with_single_equilibrium_calculation()
		system.set_condition(ThermodynamicQuantity.temperature(), 2000.0).
		for element in elements:
			system.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element), 1/len(elements))	
		
		result = system.calculate().get_value_of("G")
		result.get_value
)


