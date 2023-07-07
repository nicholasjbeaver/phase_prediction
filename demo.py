from tc_python import *





with TCPython() as start:
	property_diagram = (
		start.
		select_database_and_elements("TCHEA4", ["Hf", "Nb", "Zr"]).
		get_system().
		with_property_diagram_calculation().
		with_axis(CalculationAxis(ThermodynamicQuantity.temperature()).
			set_min(100).
			set_max(2500)).
		set_condition(ThermodynamicQuantity.mole_fraction_of_a_component("Nb"), 0.33).
		set_condition(ThermodynamicQuantity.mole_fraction_of_a_component("Hf"), 0.33).
		calculate().
		get_values_grouped_by_stable_phases_of(ThermodynamicQuantity.temperature(),
		ThermodynamicQuantity.volume_fraction_of_a_phase("ALL"))
)
property_diagram.PropertyDiagramResult.get_result_quantities()