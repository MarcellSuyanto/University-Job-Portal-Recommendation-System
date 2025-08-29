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

def get_df(format):
    match format:
        case "csv":
            return read_csv_data("data/jobs_data.csv")
        case "excel":
            return read_excel_data("data/jobs_data.xlsx")
        case "json":
            return read_json_data("data/jobs_data.json")