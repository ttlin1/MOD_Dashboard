import os
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
import textwrap

dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
budget_csv = os.path.join(dir, 'csv/MOD_Budget_dummy_actuals.csv')

df = pd.read_csv(budget_csv)
df = df.drop([7])  # dropping totals row

# Shorten column names
col_name_dict = {'Tasks and Other Activities': 'Task',
                 'MOD Grant Expenses (Budgeted)': 'MOD_budgeted',
                 'MOD Grant Expenses (Actual)': 'MOD_spent',
                 'In Kind Contributions (Budgeted)': 'In_kind_budgeted',
                 'In Kind Contributions (Actual)': 'In_kind_spent'}
df.rename(columns=col_name_dict, inplace=True)

# Change 0s to nan (to avoid division by 0 error)
df['MOD_budgeted'].replace({0: np.nan})
df['In_kind_budgeted'].replace({0: np.nan})

# Calculate new fields
df['MOD_remaining'] = df['MOD_budgeted'] - df['MOD_spent']
df['In_kind_remaining'] = df['In_kind_budgeted'] - df['In_kind_spent']
df['MOD_spent_pct'] = df['MOD_spent'] / df['MOD_budgeted']
df['MOD_remaining_pct'] = df['MOD_remaining'] / df['MOD_budgeted']
df['In_kind_spent_pct'] = df['In_kind_spent'] / df['In_kind_budgeted']
df['In_kind_remaining_pct'] = df['In_kind_remaining'] / df['In_kind_budgeted']

df = df.round(2)

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
    showlegend=True,
    title='MOD Grant Spent and Remaining Funds',
    legend=dict(
        x=0.7,
        y=1,
        traceorder='normal'
    ),
    yaxis=dict(fixedrange=True),
    xaxis=dict(tickprefix='$', tickformat='0,000', fixedrange=True),
    margin=dict(b=80, l=90, r=80, pad=5, t=160)
)

fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig)
plotly.plotly.iplot(fig, filename='MOD-budget-h-bar')
