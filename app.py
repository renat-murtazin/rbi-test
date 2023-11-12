from flask import Flask, request, jsonify
import pandas as pd
from urllib.parse import unquote

from helper import invalid_keys, prepare_datasource

app = Flask(__name__)

# Define dataset and drop empty rows
FILE_PATH = 'datasets/salary_survey.csv'
compensation_data = prepare_datasource(FILE_PATH)



@app.route('/compensation_data', methods=['GET'])
def get_compensation_data():
    
    filters = request.args.to_dict()
    fields = request.args.get('fields')
    sort_by = request.args.get('sort')

    # Apply filters
    filtered_data = apply_filters(compensation_data, filters)

    # Sort data
    sorted_data = apply_sort(filtered_data, sort_by)

    # Apply sparse fieldset
    result = apply_sparse_fieldset(sorted_data, fields)

    # Return the result as JSON
    return jsonify(result)

def apply_filters(data: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Filters data based on requested columns and values 

    Args:
        data (pd.DataFrame): _description_
        filters (dict): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        dict: filtered dataset
    """
    if not any(key in data.columns for key in filters.keys()):
        return data

    # Ensure all filter keys are valid column names
    if invalid_keys(data.columns, filters.keys()):
        raise ValueError("Invalid filter key(s)")

    for k in filters:
        filters[k] = unquote(filters[k])


    mask = pd.Series(True, index=data.index)

    for key, value in filters.items():
        mask &= (data[key] == value)

    result = data[mask]

    return result
    

def apply_sort(data: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """sorts dataframe

    Args:
        data (pd.DataFrame): filtered data source
        sort_by (str): field for sorting

    Raises:
        ValueError: checks if a sorting column exists in a dataset

    Returns:
        pd.DataFrame: sorted DataFrame
    """
    if not sort_by:
        return data

    # Ensure sort_by is a valid column name
    if sort_by not in data.columns:
        raise ValueError(f"Invalid sort_by key: {sort_by}")

    result = data.sort_values(by=sort_by)
    return result


def apply_sparse_fieldset(data: pd.DataFrame, fields: str) -> dict:
    """retreives only required fields from a dataset

    Args:
        data (pd.DataFrame): filtered / sorted datasource
        fields (str): list of fields separated by comma

    Raises:
        ValueError: _description_

    Returns:
        dict: _description_
    """
    if not fields:
        return data.to_dict(orient='records')

    # Ensure all fields are valid column names
    if invalid_keys(data.columns, fields.split(',')):
        raise ValueError(f"Invalid field(s)")

    result = data[fields.split(',')]
    return result.to_dict(orient='records')

    

if __name__ == '__main__':
    app.run(debug=True)
