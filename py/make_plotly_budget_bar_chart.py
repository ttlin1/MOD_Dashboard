import get_MOD_budget_df

import plotly
import plotly.graph_objs as go
import textwrap
import sys

sys.path.append("..")

df = get_MOD_budget_df.get_budget_df()


# Reverse sorting makes the categories draw in correct order
df.sort_index(ascending=False, inplace=True)

# Create task list with html line breaks
tasks = df['Task'].apply(lambda x: x.split(": ")[-1])
tasks = tasks.apply(lambda x: "<br>".join(textwrap.wrap(x, width=12)))


def format_pct(x):
    out_str = ' (' + '{0:.1%}'.format(x) + ')'
    out_str = out_str.replace('nan', '0')
    return out_str

# Create plotly trace objects
trace1 = go.Bar(
    y=tasks,
    x=df['MOD_spent'],
    name='MOD Grant Expenses (Spent)',
    text=df['MOD_spent_pct'].apply(format_pct),
    hoverinfo='x+text',
    orientation='h',
    marker=dict(
        color='rgba(0, 92, 40, 0.7)',
    )
)
trace2 = go.Bar(
    y=tasks,
    x=df['MOD_remaining'],
    name='MOD Grant Expenses (Remaining)',
    text=df['MOD_remaining_pct'].apply(format_pct),
    hoverinfo='x+text',
    orientation='h',
    marker=dict(
        color='rgba(0, 92, 40, 0.4)',
    )
)
trace3 = go.Bar(
    y=tasks,
    x=df['In_kind_spent'],
    name='In Kind Contributions (Spent)',
    text=df['In_kind_spent_pct'].apply(format_pct),
    hoverinfo='x+text',
    orientation='h',
    marker=dict(
        color='rgba(8, 76, 141, 0.7)',
    )
)
trace4 = go.Bar(
    y=tasks,
    x=df['In_kind_remaining'],
    name='In Kind Contributions (Remaining)',
    text=df['In_kind_remaining_pct'].apply(format_pct),
    hoverinfo='x+text',
    orientation='h',
    marker=dict(
        color='rgba(8, 76, 141, 0.4)',
    )
)

data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    barmode='stack',
    hovermode='closest',
    showlegend=True,
    title='MOD Grant Spent and Remaining Funds',
    font=dict(size=14),
    legend=dict(
        x=0.7,
        y=1,
        traceorder='normal'
    ),
    yaxis=dict(fixedrange=True),
    xaxis=dict(tickprefix='$', tickformat='0,000', fixedrange=True),
    margin=dict(b=80, l=120, r=80, pad=5, t=160)
)

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig)
plotly.plotly.iplot(fig, filename='MOD-budget-h-bar')
