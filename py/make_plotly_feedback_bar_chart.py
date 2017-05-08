import get_OTP_feedback_df
import plotly
import plotly.graph_objs as go
import os
from os.path import join
#from palettable.colorbrewer.qualitative import Set3_12
from bokeh import palettes

root_dir = os.path.dirname(os.path.dirname(__file__))
in_file = join(root_dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
print in_file
print root_dir
df = get_OTP_feedback_df.get_feedback_df(in_file)


g = df.groupby('Primary Issue')\
        .apply(lambda df: df['Primary Issue'].resample('1M').count())
g = g.unstack('Primary Issue').fillna(0)

data = []
counter = 0
columns = g.columns.values.tolist()

colors = palettes.Category20[len(columns)]
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
