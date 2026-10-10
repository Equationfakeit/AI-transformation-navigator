import unittest

from engine import DIMENSIONS, RoiInputs, calculate_roi, opportunities, readiness_score, strategy_report


class ReadinessTests(unittest.TestCase):
    def test_all_one_is_zero(self):
        self.assertEqual(readiness_score({name: 1 for name in DIMENSIONS}), 0)

    def test_all_five_is_hundred(self):
        self.assertEqual(readiness_score({name: 5 for name in DIMENSIONS}), 100)

    def test_midpoint(self):
        self.assertEqual(readiness_score({name: 3 for name in DIMENSIONS}), 50)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            readiness_score({name: 9 for name in DIMENSIONS})

    def test_ranking(self):
        ranked = opportunities("Manufacturing", 60)
        self.assertEqual(len(ranked), 6)
        self.assertTrue(all(0 <= x["priority"] <= 100 for x in ranked))
        self.assertEqual([x["priority"] for x in ranked], sorted([x["priority"] for x in ranked], reverse=True))


class RoiTests(unittest.TestCase):
    def test_reproducible_default(self):
        result = calculate_roi(RoiInputs())
        self.assertAlmostEqual(result.annual_hours_released, 2304)
        self.assertAlmostEqual(result.annual_gross_capacity_value, 80640)
        self.assertAlmostEqual(result.annual_net_capacity_value, 62640)
        self.assertAlmostEqual(result.first_year_net_value, 22640)
        self.assertAlmostEqual(result.first_year_roi_pct, 56.6)
        self.assertEqual(len(result.cumulative_cash_equivalent), 4)

    def test_no_benefit_means_no_payback(self):
        result = calculate_roi(RoiInputs(adoption_rate=0.0))
        self.assertIsNone(result.payback_months)
        self.assertLess(result.first_year_net_value, 0)

    def test_zero_initial_cost(self):
        result = calculate_roi(RoiInputs(one_time_cost_usd=0.0))
        self.assertIsNone(result.first_year_roi_pct)

    def test_reject_invalid(self):
        with self.assertRaises(ValueError):
            calculate_roi(RoiInputs(adoption_rate=1.5))

    def test_report_contains_disclosure(self):
        ratings = {name: 3 for name in DIMENSIONS}
        ranked = opportunities("Manufacturing", 50)
        model = RoiInputs()
        result = calculate_roi(model)
        report = strategy_report("Demo", "Manufacturing", 200, ratings, ranked, model, result)
        self.assertIn("not equivalent to realized cash savings", report)
        self.assertIn("not affiliated with Deloitte", report)


if __name__ == "__main__":
    unittest.main()
