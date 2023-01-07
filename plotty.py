import pandas as pd
import plotly.express as px

df = pd.read_csv('fmr_plottable.csv')
df = df.dropna()
# plot based on lat and long
fig = px.scatter_geo(df,lat='LAT',lon='LONG', hover_name="ZIP", size="TWO_BEDROOM", projection="natural earth")
fig.update_layout(title = 'World map ( to be converted to the us only)', title_x=0.5)
# export to an image

fig.write_image("map.png")
