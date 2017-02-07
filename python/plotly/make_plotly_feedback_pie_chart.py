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

x = fb_df.groupby(['Type of Feedback']).agg({'Type of Feedback': 'count'})

fig = {
    'data': [{'labels': x.index,
              'values': x.values,
              'type': 'pie',
              "hole": 0.4,
              "hoverinfo": "label+percent+name",
              "textposition": "inside",
#              'marker': {'colors': ['#66C5CC', '#F6CF71',
#                                    '#F89C74', '#DCB0F2',
#                                    '#87C55F', '#9EB9F3',
#                                    '#FE88B1']
#                         },
              }],
    'layout': {
        'title': 'Type of Feedback',
        }
     }

plotly.offline.plot(fig)
# plotly.plotly.iplot(fig, filename='type of feedback pie')
