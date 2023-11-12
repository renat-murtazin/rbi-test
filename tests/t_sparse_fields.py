import unittest
import pandas as pd
from app import apply_sparse_fieldset

class TestApplySparseFieldsetFunction(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['John', 'Jane', 'Bob'],
            'salary': [100000, 120000, 90000]
        })

    def test_apply_sparse_fieldset_valid(self):
        fields = 'id,salary'
        result = apply_sparse_fieldset(self.data, fields)
        expected_result = [{'id': 1, 'salary': 100000},
                           {'id': 2, 'salary': 120000},
                           {'id': 3, 'salary': 90000}]
        self.assertEqual(result, expected_result)

    def test_apply_sparse_fieldset_empty(self):
        fields = ''
        result = apply_sparse_fieldset(self.data, fields)
        expected_result = self.data.to_dict(orient='records')
        self.assertEqual(result, expected_result)

    def test_apply_sparse_fieldset_invalid_fields(self):
        fields = 'position,bonus'
        with self.assertRaises(ValueError) as context:
            apply_sparse_fieldset(self.data, fields)
        self.assertIn("Invalid field(s)", str(context.exception))



if __name__ == '__main__':
    unittest.main()
