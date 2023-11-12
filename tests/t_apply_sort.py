import unittest
import pandas as pd
from app import apply_sort

class TestApplySortFunction(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'id': [2, 1, 3],
            'name': ['Jane', 'John', 'Bob'],
            'salary': [120000, 100000, 90000]
        })

    def test_apply_sort_valid(self):
        sort_by = 'salary'
        result = apply_sort(self.data, sort_by)
        expected_result = [{'id': 3, 'name': 'Bob', 'salary': 90000},
                           {'id': 1, 'name': 'John', 'salary': 100000},
                           {'id': 2, 'name': 'Jane', 'salary': 120000}]
        self.assertEqual(result, expected_result)

    def test_apply_sort_empty(self):
        sort_by = ''
        result = apply_sort(self.data, sort_by)
        expected_result = self.data.to_dict(orient='records')
        self.assertEqual(result, expected_result)

    def test_apply_sort_invalid_key(self):
        sort_by = 'position'
        with self.assertRaises(ValueError) as context:
            apply_sort(self.data, sort_by)
        self.assertIn("Invalid sort_by key", str(context.exception))



if __name__ == '__main__':
    unittest.main()
