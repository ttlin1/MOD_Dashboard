import pandas as pd
import plotly
import os
import numpy as np
from os.path import join


dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
in_file = join(dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
df = pd.read_excel(in_file, "Sheet1")

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


x = df.groupby(['Primary Issue']).agg({'Primary Issue': 'count'})
labs = x.index.tolist()
vals = [item for sublist in x.values for item in sublist]

fig = {
    'data': [{'labels': labs,
              'values': vals,
              'type': 'pie',
              # "hole": 0.4,
              "hoverinfo": "label+value",
              "textposition": "inside",
              "sort": False,
              "direction": "clockwise",
              'marker': {'colors': ['#8dd3c7', '#ffffb3', '#bebada',
                                    '#FFAC92', '#80b1d3', '#fdb462',
                                    '#DBF498', '#fccde5', '#d9d9d9',
                                    '#DDA7DD', '#A0E89C']
                         },
              }],
    'layout': {"hovermode": "closest", 
               "font": dict(size=16),
        }
     }


plotly.offline.plot(fig)
plotly.plotly.iplot(fig, filename='type of feedback pie')
