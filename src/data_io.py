import json
import os
import pandas as pd

def save_json_file(data,file_path):
    """ 
    Save a Python dictionary as a JSON file. 
    Args: 
        data (dict): The data to save. 
        file_path (str): The path of the JSON file. 
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True) #os.path.dirname(file_path)=data/raw
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    
def load_json_file(file_path):
    """ 
    Load data from a JSON file. 
    Args: 
        file_path (str): The path of the JSON file. 
    Returns: 
        dict: The JSON data loaded as a Python dictionary. 
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_csv_file(df,file_path):
    """ 
    Save a pandas DataFrame as a CSV file. 
    Args: 
        df (pandas.DataFrame): The DataFrame to save. 
        file_path (str): The path of the CSV file. 
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False, encoding="utf-8")


def load_csv_file(file_path):
    """ 
    Load data from a CSV file. 
    Args: 
        file_path (str): The path of the CSV file. 
    Returns: 
        pandas.DataFrame: The loaded CSV data. 
    """
    df = pd.read_csv(file_path)
    return df