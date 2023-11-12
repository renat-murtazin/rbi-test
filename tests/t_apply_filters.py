import unittest
import pandas as pd
from app import apply_filters

class TestApplyFiltersFunction(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['John', 'Jane', 'Bob'],
            'salary': [100000, 120000, 90000]
        })

    def test_apply_filters_valid(self):
        filters = {'salary': 120000}
        result = apply_filters(self.data, filters)
        expected_result = [{'id': 2, 'name': 'Jane', 'salary': 120000}]
        self.assertEqual(result, expected_result)

    def test_apply_filters_empty(self):
        filters = {}
        result = apply_filters(self.data, filters)
        expected_result = self.data.to_dict(orient='records')
        self.assertEqual(result, expected_result)

    def test_apply_filters_invalid_keys(self):
        filters = {'position': 'Manager'}
        with self.assertRaises(ValueError) as context:
            apply_filters(self.data, filters)

        self.assertIn("Invalid filter key(s)", str(context.exception))

if __name__ == '__main__':
    unittest.main()