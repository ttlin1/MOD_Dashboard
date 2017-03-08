# -*- coding: utf-8 -*-
"""
Make MOD Grant Gantt Chart - Madeline Steele for TriMet, 2017
"""

import os
import pandas as pd
import plotly
import datetime
from plotly import figure_factory as FF


def to_unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
gantt_csv = os.path.join(dir, 'csv/mod_grant_gantt.csv')
df = pd.read_csv(gantt_csv)

# This plotly function does most othe work but it not too
# flexibles - I customize below by manipulating the object it creates

# Weirdly, the boxes get vertically flipped unless the "group_tasks" parameter
# is set to True. As of 2/10/2017, on Windows, pip or conda install plotly
# pulls an older version that does not include this essential parameter. I
# had to use this command to install the latest greatest:
# pip install git+https://github.com/plotly/plotly.py.git
# This was not an issue on my mac at home, forwhatever reason.

fig = FF.create_gantt(df, colors=['#a1dab4', '#253494'],
                      index_col='Complete',
                      show_colorbar=True,
                      bar_width=0.2,
                      showgrid_x=True,
                      showgrid_y=True,
                      height=750,
                      width=1188,
                      group_tasks=True
                      )

margin_dict = {
      "r": 80,
      "b": 80,
      "pad": 5,
      "l": 340,
      "t": 5
    }

fig['layout']['margin'] = margin_dict
fig['layout']['font'] = dict(size=14)
del fig['layout']['title']
fig['data'][-1].items()[0][1]["colorbar"] = {"title": "Percent Complete"}
fig['layout']['hovermode'] = 'closest'  # "x" | "y" | "closest" | False
fig['layout']['xaxis']['fixedrange'] = True
time_range = [to_unix_time(datetime.datetime(2016, 12, 20)),
              to_unix_time(datetime.datetime(2019, 1, 1))]
fig['layout']['xaxis']['range'] = time_range

# Removing the range selector buttons - not that helpful
del fig['layout']['xaxis']['rangeselector']


fig['layout']['yaxis']['fixedrange'] = True
fig['layout']['yaxis']['tickmode'] = 'array'
labels = df['Task'].apply(lambda x: '' if ':' in x else x)
fig['layout']['yaxis']['ticktext'] = labels
fig['layout']['yaxis']['tickvals'] = range(len(df['Task']) - 1, -1, -1)

# I really want to show the 6 task groups as having a higher visual
# hierarchy - the rest of the script (and extra lines in the csv) are
# my way of accomplishing that using annotations
bold_task_labels = []
for i in range(0, len(df)):
    trace = fig['data'][i]
    if trace['x'] == ['2017-01-01', '2017-01-01']:
        trace['hoverinfo'] = 'none'
        if 'dummy' not in df['Task'][i]:
            bold_task_labels.append(
                    dict(
                        x=-.005,
                        y=len(df) - i - 1,
                        xanchor='right',
                        xref='paper',
                        yref='y',
                        text='<b>' + df['Task'][i] + '</b>',
                        showarrow=False,
                        ax=0,
                        ay=-40,
                        font={'size': 14}
                        )
                    )
    else:
        trace['text'] = str(df['Complete'][i]) + '% complete'
        trace['hoverinfo'] = 'text'
fig['layout']['annotations'] = bold_task_labels

plotly.offline.plot(fig)
#plotly.plotly.iplot(fig,
#                    filename='MOD_Grant_gantt_chart',
#                    world_readable=True)
