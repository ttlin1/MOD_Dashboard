import pandas as pd
import plotly
import plotly.graph_objs as go
import sys

sys.path.append("..")
import get_MOD_budget_df

df = get_MOD_budget_df.get_budget_df()

df.sort_index(ascending=False, inplace=True)

mod_tasks = df['Task'].apply(lambda x: x.split(": ")[-1]) + ' (MOD)'
ik_tasks = df['Task'].apply(lambda x: x.split(": ")[-1]) + ' (In Kind)'
tasks = mod_tasks.append(ik_tasks)
budgeted = df['MOD_budgeted'].append(df['In_kind_budgeted'])

pie_df = pd.concat([tasks, budgeted], axis=1)
pie_df.sort_index(ascending=True, inplace=True)
pie_df.columns = ['Task', 'USD']
pie_df = pie_df[pie_df['USD'] != 0]
pie_df['pct'] = pie_df['USD'] / pie_df['USD'].sum()
pie_df['pct'] = pie_df['pct'].apply(lambda x: '{0:.1f}%'.format(x*100))

# Create task list with html line breaks
tasks = pie_df['Task'].apply(lambda x: x.split(": ")[-1])
#tasks = tasks.apply(lambda x: "<br>".join(textwrap.wrap(x, width=20)))


# 5F6FC2 = old version of color 3
# colors = ['#BD7CB4', '#DAADD4', '#6677D0', '#7D89CB', '#56C4C5', '#82DDDD',
#           '#ADD68A', '#CEEAB7', '#FCC777', '#FFD89E', '#FFB19F', '#999999']

money_text = pie_df['USD'].apply(lambda x: '${:,}'.format(x))\

trace1 = {
  "direction": "clockwise",
  "hoverinfo": "label+text+percent",
  "labels": tasks,
  "marker": {
    "colors": ["#BD7CB4", "#DAADD4", "#6E80E0", "#95A3EE", "#56C4C5",
               "#82DDDD", "#ADD68A", "#CEEAB7", "#FCC777", "#FFD89E",
               "#FFB19F", "#999999"],
  },
  "showlegend": True,
  "sort": False,
  "text": money_text,
  "textinfo": 'percent',
  "textposition": "auto", #"inside" | "outside" | "auto" | "none" 
  "type": "pie",
  "values": pie_df['USD']
}
data = go.Data([trace1])
layout = {"margin": {
                    "r": 120,
                    "l": 145,
                    "t": 160
                    },
          "font": {"size": 16},
          "title": "MOD Grant Budget"
          }
fig = go.Figure(data=data, layout=layout)


plotly.offline.plot(fig)
#plotly.plotly.iplot(fig, filename='MOD-budget-pie')
