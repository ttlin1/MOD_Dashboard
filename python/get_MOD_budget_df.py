from __future__ import print_function
import gspread
import pandas as pd
import numpy as np
from oauth2client import file

def get_budget_df():
    # Get Google Sheets API credentials
    store = file.Storage('P:\\sheets_storage.json')
    creds = store.get()
    
    # Get budget tracking sheet content
    docid = r"1cOiS3_yZlO63mhdyoYDE2A-WPyu6T1vc6YCHiVlQ8Dc"
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(docid)
    data = spreadsheet.worksheets()[0].get_all_values()
    
    # Convert data from sheet to dataframe
    df = pd.DataFrame(data)
    df.columns = df.iloc[0] # use first row as column names
    df = df.reindex(df.index.drop([0,8,9])) # drop first row and totals rows
    df['Task'] = df['Task'].apply(lambda x: x.split("\n")[0].strip())
    
    # Shorten column names
    col_name_dict = {'Budgeted MOD Sandbox Federal Amount ($)': 'MOD_budgeted',
                     'Spent MOD Sandbox Federal Amount ($)': 'MOD_spent',
                     'Remaining MOD Sandbox Federal Amount ($)': 'MOD_remaining',
                     'MOD Sandbox Cost Share ($)': 'In_kind_budgeted',
                     'Spent MOD Sandbox Cost Share ($)': 'In_kind_spent',
                     'Remaining MOD Sandbox Cost Share ($)': 'In_kind_remaining'}
    df.rename(columns=col_name_dict, inplace=True)
    
    for col_name in list(df.columns.values[2:]):
        df[col_name].replace('[\$,)]', '', regex=True, inplace=True)
        df[col_name].replace('[(]','-', regex=True, inplace=True)
        df[col_name] = df[col_name].astype(float).fillna(0.0)
    
    # Change 0s to nan (to avoid division by 0 error)
    df['MOD_budgeted'].replace({0: np.nan})
    df['In_kind_budgeted'].replace({0: np.nan})
        
    # Calculate new fields
    df['MOD_spent_pct'] = df['MOD_spent'] / df['MOD_budgeted']
    df['MOD_remaining_pct'] = df['MOD_remaining'] / df['MOD_budgeted']
    df['In_kind_spent_pct'] = df['In_kind_spent'] / df['In_kind_budgeted']
    df['In_kind_remaining_pct'] = df['In_kind_remaining'] / df['In_kind_budgeted']
    df = df.round(2)
    
    return df

if __name__ == '__main__':
    get_budget_df()
