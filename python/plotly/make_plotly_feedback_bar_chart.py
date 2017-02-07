# -*- coding: utf-8 -*-
"""
cleaning up the feedback tracking spreadsheet
"""

import pandas as pd
import plotly
import plotly.graph_objs as go
import os
from os.path import join

# fb short for feedback here

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
in_file = join(dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
fb_df = pd.read_excel(in_file, "Sheet1")

# x = fb_df.groupby(['Type of Feedback']).agg({'Type of Feedback': 'count'})

df = fb_df.set_index('Date Received')
weekly = df['Type of Feedback'].resample('1W').count()


data = [
    go.Bar(
        x=weekly.index,
        y=weekly.values
    )
]

plotly.offline.plot(data)
# plotly.plotly.iplot(data, filename='feedback histogram')
