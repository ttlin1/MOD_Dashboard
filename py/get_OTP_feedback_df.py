import pandas as pd
import numpy as np


def get_feedback_df(in_excel):

    df = pd.read_excel(in_excel, "Sheet1")

    # In some columns, I added semicolon separated lists of issues. Just grabbing the first for now.
    df['Primary Concern or Request'] = df['Primary Concern or Request'].str.split(';').str[0]
    df['Underlying Issue'] = df['Underlying Issue'].str.split(';').str[0]

    df['Primary Issue'] = df['Type of Feedback']
    
    # If the type of feedback is a complaint, go down a level of detail
    df['Primary Issue'][df['Type of Feedback'] == 'Complaint'] = \
        df['Primary Concern or Request']
    
    # If they are "Unhappy with Trip Plan", go down another level
    df['Primary Issue'][(df['Primary Issue'] == 'Unhappy with trip plan') \
       & pd.notnull(df['Underlying Issue'])] = df['Underlying Issue']
    
    df = df.set_index('Date Received')
    df = df[['Primary Issue', 'Underlying Issue']]
    
    x = df.groupby('Primary Issue').aggregate(np.count_nonzero)
    categories_to_lump = x[x['Underlying Issue'] < 10].index.tolist()
    
    # Lump issues with fewer than 10 occurences into "Other Complaints"
    for index, row in df.iterrows():
        if row['Primary Issue'] in categories_to_lump:
            row['Primary Issue'] = 'Other complaint'
    
    return df
                        
if __name__ == '__main__':
    get_feedback_df()
