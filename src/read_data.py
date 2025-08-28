import pandas as pd


def read_csv_data(path):
    df = pd.read_csv(path)
    return df

def read_excel_data(path):
    df = pd.read_excel(path)
    return df

def read_json_data(path):
    df = pd.read_json(path)
    return df

