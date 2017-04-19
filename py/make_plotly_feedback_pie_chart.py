import get_OTP_feedback_df
import plotly
import os
from os.path import join
from palettable.colorbrewer.qualitative import Set3_12

root_dir = os.path.dirname(os.path.dirname(__file__))
in_file = join(root_dir, 'xlsx/OTP_feedback_tracking_cleaned_no_pi.xlsx')
print in_file
print root_dir
df = get_OTP_feedback_df.get_feedback_df(in_file)

x = df.groupby(['Primary Issue']).agg({'Primary Issue': 'count'})
labs = x.index.tolist()
vals = [item for sublist in x.values for item in sublist]
val_text = ["Total count: " + str(val) for val in vals]

colors = Set3_12.hex_colors

fig = {
    'data': [{'labels': labs,
              'values': vals,
              'type': 'pie',
              # "hole": 0.4,
              "text": val_text,
              "hoverinfo": "label+text",
              "textinfo": 'percent',
              "textposition": "inside",
              "sort": False,
              "direction": "clockwise",
              'marker': {'colors': colors
                         },
              }],
    'layout': {"hovermode": "closest", 
               "font": dict(size=16),
        }
     }


plotly.offline.plot(fig)
#plotly.plotly.iplot(fig, filename='type of feedback pie')
