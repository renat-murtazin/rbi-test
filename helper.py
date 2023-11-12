import pandas as pd

def invalid_keys(df_keys, filter_keys) -> bool:
    """Checks if a list of given filter columns is correct

    Args:
        df_keys (Series): List of columns in a Dataset
        filter_keys (list): column names from a request

    Returns:
        bool: returns False if the correct column names are provided
    """
    if set(filter_keys).issubset(set(df_keys)):
        return False
    
    return True


def prepare_datasource(file_path) -> pd.DataFrame:

    df = pd.read_csv(file_path)

    if df.empty:
        raise ("DataFrame is empty")
    
    # column mapping
    df.columns = [
        'timestamp', 'employment_type', 'company_name', 
        'company_size', 'country', 'city',
        'industry', 'company_type', 'experience_industry', 
        'experience_current_company', 'job_title', 'job_ladder',
        'job_level', 'required_hours', 'actual_hours',
        'education_level', 'salary', 'bonus',
        'stock_options', 'health_insurance_offered', 'annual_vacation_weeks',
        'happy_at_position', 'plan_to_resign', 'industry_direction_thoughts', 
        'gender', 'top_skills_for_growth', 'bootcamp_done'
    ]

    # drop empty rows
    df = df.dropna()

    # basic data manipulation
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    salary_columns = ['salary', 'bonus', 'stock_options']
    df[salary_columns] = df[salary_columns].replace('[\$,]', '', regex=True).astype(float)

    df['country'] = df['country'].str.replace(r'\s*\([^)]*\)\s*', '')
    df['country_code'] = df['country'].str.extract(r'\(([^)]+)\)')
    df['city'] = df['city'].str.split(',| ').str[0]

    return df
