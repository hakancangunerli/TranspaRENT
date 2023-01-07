using Pkg
using DataFrames
using PyCall
# Pkg.add("CSV")
using CSV


py"""
# for scraping call beautifulsoup
from bs4 import BeautifulSoup
import requests 
import pandas as pd
import lxml


# https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2023_code/2023summary.odn?fips=1312199999&year=2023&selection_type=county&fmrtype=Final

URL = 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2023_code/2023summary.odn?fips=1312199999&year=2023&selection_type=county&fmrtype=Final'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find('table', class_='big_table')
df = pd.read_html(results.prettify())
# export it to a csv file
df[0].to_csv('fmr.csv')
"""



# read in the csv file
df = CSV.read("fmr.csv", DataFrame)

# drop the first column 
df = df[:, 2:end]

df
rename!(df, [:ZIP, :EFFICIENCY, :ONE_BEDROOM, :TWO_BEDROOM, :THREE_BEDROOM, :FOUR_BEDROOM,])

# remove first row 
df = df[2:end, :]

# convert each column to integers 

df[!, :ZIP] = parse.(Int64, df[!, :ZIP])
# remove the $ sign from the strings

df

# replace $ and , 
columns_names = ["EFFICIENCY",	"ONE_BEDROOM",	"TWO_BEDROOM"	,"THREE_BEDROOM"	,"FOUR_BEDROOM"]

for i in columns_names
    df[!, i] = replace.(df[!, i], r"\$" => "")
    df[!, i] = replace.(df[!, i], r"\," => "")
    df[!, i] = parse.(Int64, df[!, i])
end
df


# install pgeocode from pycall 


pg = pyimport_conda("pgeocode", "pgeocode")
nomi = pg.Nominatim("us")

# get the latitude and longitude for each zip code
lat = []
long = []
for i in df[!, :ZIP]
    lat = push!(lat, nomi.query_postal_code(i).latitude)
    long = push!(long, nomi.query_postal_code(i).longitude)
end

# add the latitude and longitude to the dataframe
df[!, :LAT] = lat
df[!, :LONG] = long


df

# export the dataframe to a csv file
CSV.write("fmr_plottable.csv", df)

# call the plotty.py file from the command line 
run(`python plotty.py`)

# remove the csv file
rm("fmr_plottable.csv")

