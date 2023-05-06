# %%
# for scraping call beautifulsoup
from bs4 import BeautifulSoup
import requests 
import pandas as pd

# https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2023_code/2023summary.odn?fips=1312199999&year=2023&selection_type=county&fmrtype=Final

# URL = 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2023_code/2023summary.odn?fips=1312199999&year=2023&selection_type=county&fmrtype=Final'

# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find('table', class_='big_table')

# %%
# df = pd.read_html(results.prettify())

# %%
# export it to a csv file
# df[0].to_csv('fmr.csv')

# %%
df = pd.read_csv('fmr.csv')

# %%

# remove the first row 
df = df.drop([0])

# %%
# remove all text that say 'Atlanta-Sandy Springs-Roswell, GA HUD Metro FMR Area Small Area FMRs'
df = df[df['Unnamed: 0'] != 'Atlanta-Sandy Springs-Roswell, GA HUD Metro FMR Area Small Area FMRs']

# %%
df = df.drop(['Unnamed: 0'], axis=1)    

# %%
# change titles to Effiiency, One Bedroom, Two Bedroom, Three Bedroom, Four Bedroom, Five Bedroom
df.columns = ['ZIP Code', 'Efficiency', 'One Bedroom', 'Two Bedroom', 'Three Bedroom', 'Four Bedroom']

# %%
# convert dollars to integers

for col in df.columns:
    df[col] = df[col].str.replace('$', '')
    df[col] = df[col].str.replace(',', '')
    df[col] = df[col].astype(int)
df

# %%
# make a map of the zip codes and the fmr, only have georgia zip codes
# !pip install pgeocode
import pgeocode


# %%

nomi = pgeocode.Nominatim('us')
# get long and lat for zip codes
df['latitude'] = df['ZIP Code'].apply(lambda x: nomi.query_postal_code(x).latitude)
df['longitude'] = df['ZIP Code'].apply(lambda x: nomi.query_postal_code(x).longitude)

# %%
df

# %%
df

# %%
df = df.dropna()

# plot based on lat and long
fig = px.scatter_geo(df,lat='latitude',lon='longitude', hover_name="ZIP Code", size="Two Bedroom", projection="natural earth")
fig.update_layout(title = 'World map ( to be converted to the us only)', title_x=0.5)
# export to an image

fig.write_image("map.png")


# show the map on markdown

# %% [markdown]
# <!-- embed png image -->
# ![](./map.png)


