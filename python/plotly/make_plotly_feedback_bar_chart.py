# -*- coding: utf-8 -*-
"""
cleaning up the feedback tracking spreadsheet
"""

import pandas as pd
import plotly
import plotly.graph_objs as go
import os
from os.path import join
import numpy as np

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
in_file = join(dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
df = pd.read_excel(in_file, "Sheet1")

# x = fb_df.groupby(['Type of Feedback']).agg({'Type of Feedback': 'count'})

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

g = df.groupby('Primary Issue')\
        .apply(lambda df: df['Primary Issue'].resample('1W').count())

g = g.unstack('Primary Issue').fillna(0)

# From color brewer (with red toned down).
colors = ['#A0E89C', '#DDA7DD', '#d9d9d9', '#fccde5', '#DBF498',
          '#fdb462', '#80b1d3', '#FFAC92', '#bebada', '#ffffb3', '#8dd3c7']

# Alternative pallete - Rainbow (reversed)
# ['#F5A872', '#FCC777', '#FBF583', '#ADD68A', '#64C195', '#56C4C5',
#    '#5C88C5', '#5664AF', '#7E6AAF', '#BD7CB4']

data = []
counter = 0
columns = g.columns.values.tolist()
columns.reverse()
for column in columns:
    # color = colors[counter]
    data.append(
        go.Bar(
            y=g[column],
            x=g.index,
            name=column,
            text=column,
            textfont={"size": 20},
            marker={"color": colors[counter]},
            hoverinfo="y+name"
        )
    )
    counter += 1


layout = go.Layout(
    barmode='stack',
    hovermode='closest',
    xaxis=dict(fixedrange=True),
    font=dict(size=16)
)

fig = go.Figure(data=data, layout=layout)


plotly.offline.plot(fig)
plotly.plotly.iplot(fig, filename='feedback histogram')
