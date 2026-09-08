import unittest

from app.knowledge.relationship_graph import match_relationships
from app.models.schemas import EnvironmentalInput


class RelationshipGraphTests(unittest.TestCase):
    def test_worked_example_matches_compound_rule(self):
        user_input = EnvironmentalInput(
            soil_organic_carbon_pct=0.3,
            rainfall="low",
            land_use_type="monoculture wheat",
            region_type="semi-arid",
        )

        ids = {relationship["id"] for relationship in match_relationships(user_input)}

        self.assertIn("compound_semi_arid_low_soc_monoculture_transition", ids)
        self.assertIn("agroforestry_increases_avian_richness", ids)

    def test_compound_rule_needs_every_environmental_condition(self):
        incomplete = EnvironmentalInput(
            soil_organic_carbon_pct=0.3,
            rainfall="moderate",
            land_use_type="monoculture wheat",
            region_type="semi-arid",
        )

        ids = {relationship["id"] for relationship in match_relationships(incomplete)}

        self.assertNotIn("compound_semi_arid_low_soc_monoculture_transition", ids)

    def test_previously_unused_inputs_now_trigger_rules(self):
        user_input = EnvironmentalInput(
            soil_moisture="low",
            temperature_c=34,
            species_richness="declining",
        )

        ids = {relationship["id"] for relationship in match_relationships(user_input)}

        self.assertIn("low_soil_moisture_requires_water_retention_practices", ids)
        self.assertIn("high_temperature_aridity_feedback", ids)
        self.assertIn("low_species_richness_habitat_complexity_recovery", ids)


if __name__ == "__main__":
    unittest.main()
