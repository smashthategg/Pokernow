import plotly.express as px
import stats

x = []
y = []

df = stats.__dict__['df']

for player in df:
    if df[player]['numhands'] >= 10:
        x.append(df[player]['VPIP'])
        y.append(df[player]['SD'])

'''
fig = px.scatter(x, y)
fig.show()
'''

fig = px.histogram(df, x, labels={'x':'VPIP'}, nbins = 50, title = "Distribution of VPIP Among Players")
fig.show()