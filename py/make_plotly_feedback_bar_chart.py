import get_OTP_feedback_df

import plotly
import plotly.graph_objs as go
import os
from os.path import join
from palettable.colorbrewer.qualitative import Set3_12


root_dir = os.path.dirname(os.path.dirname(__file__))
in_file = join(root_dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
print in_file
print root_dir
df = get_OTP_feedback_df.get_feedback_df(in_file)


g = df.groupby('Primary Issue')\
        .apply(lambda df: df['Primary Issue'].resample('1W').count())

g = g.unstack('Primary Issue').fillna(0)

# From color brewer (with red toned down).
# colors = ['#A0E89C', '#DDA7DD', '#d9d9d9', '#fccde5', '#DBF498',
#           '#fdb462', '#80b1d3', '#FFAC92', '#bebada', '#ffffb3', '#8dd3c7']
#
# Alternative pallete - Rainbow (reversed)
# ['#F5A872', '#FCC777', '#FBF583', '#ADD68A', '#64C195', '#56C4C5',
#    '#5C88C5', '#5664AF', '#7E6AAF', '#BD7CB4']

data = []
counter = 0
columns = g.columns.values.tolist()
colors = Set3_12.hex_colors
colors.reverse()
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
