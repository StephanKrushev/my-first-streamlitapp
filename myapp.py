# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df



int_df_raw = load_data(path="./data/share-of-individuals-using-the-internet.csv")
ds_e3 = deepcopy(int_df_raw)
ds_e3.rename(columns={'Individuals using the Internet (% of population)':'Internet_Usage'}, inplace=True)

# Add title and header
st.title("Individuals using the Internet")


# Setting up rows
# 3 rows, 1 column



st.subheader("Percentile usage per country")
# Widgets: selectbox
percentiles = ["Initial", '20%', '50%', '80%', '99%']
percentile = st.selectbox("Choose a percentile", percentiles)

if percentile == "Initial":
    perc=0
elif percentile == '20%':
    perc=20
elif percentile == '50%':
    perc=50
elif percentile == '80%':
    perc=80
else:
    perc=99



ds_e3_min = ds_e3[ds_e3['Internet_Usage']>perc].groupby('Entity').agg({'Year':'min'}).reset_index()

fig = px.choropleth(ds_e3_min.sort_values('Year'),
                locations='Entity',
                locationmode='country names',
                color='Year',
                hover_data=['Entity', 'Year'],
                animation_frame='Year',
                color_continuous_scale='Viridis',
                range_color=[min(ds_e3_min['Year']), max(ds_e3_min['Year'])])


# Update layout
fig.update_layout(title='Internet Usage by Country', 
                coloraxis_colorbar=dict(title='Year'), 
                coloraxis_colorbar_len=0.5, 
                coloraxis_colorbar_x=1.1, 
                margin={"r":0,"t":0,"l":0,"b":0})

# Show the plot

st.plotly_chart(fig)



st.subheader("Percentile usage per country during Color revolutions and Arab Spring")
revolutions = ["Color", "Arab Spring"]      
revolution = st.selectbox("Choose a revolution", revolutions)

data = {'Entity': ['Tunisia', 'Algeria', 'Jordan', 
                'Oman', 'Saudi Arabia', 'UAE', 
                'Egypt',  'Syria', 'Yemen', 
                'Djibouti', 'Sudan', 'Palestine', 
                'Iraq', 'Bahrain', 'Libya', 
                'Kuwait', 'Morocco', 'Mauritania', 'Lebanon'],
    'Year': [2010, 2010, 2011, 
                2011, 2011, 2011, 
                2011, 2011, 2011, 
                2011, 2011, 2011, 
                2011, 2011, 2011,
                2011, 2011, 2011, 2011],
    'Type': ['spring', 'spring', 'spring',
                'spring', 'spring', 'spring',
                'spring', 'spring', 'spring',
                'spring', 'spring', 'spring',
                'spring', 'spring', 'spring',
                'spring', 'spring', 'spring', 'spring']
                        }
ds_e3_arab = pd.DataFrame(data)

data = {'Entity': ['Armenia', 'Georgia',  'Ukraine', 'Uzbekistan', 
                'Moldova', 'Kyrgyzstan', 'Azerbaijan', 'Belarus',
                'Serbia'],
    'Year': [2004, 2003, 2004, 2005, 
                2003, 2005, 2003, 2002, 
                2000],
    'Type': ['color', 'color', 'color', 'color', 
                'color', 'color', 'color', 'color', 
                'color'
    ]        }
ds_e3_color = pd.DataFrame(data)

ds_e3_arab_int = ds_e3_arab.merge(ds_e3, on=['Entity', 'Year'], how='left').dropna()
ds_e3_color_int = ds_e3_color.merge(ds_e3, on=['Entity', 'Year'], how='left').dropna()
ds_e3_color_arab_int = pd.concat([ds_e3_color_int, ds_e3_arab_int])




if revolution == "Color":
    rev_type = "color"
else:
    rev_type = "spring"



fig2 = px.choropleth(ds_e3_color_arab_int[ds_e3_color_arab_int['Type']==rev_type].sort_values('Year'),
                locations='Entity',
                locationmode='country names',
                color='Internet_Usage',
                hover_data=['Entity', 'Year', 'Internet_Usage'],
                animation_frame='Year',
                color_continuous_scale='Viridis',
                range_color= [min(ds_e3_color_arab_int['Internet_Usage']), max(ds_e3_color_arab_int['Internet_Usage'])])  
# Update layout
fig2.update_layout(title='Internet Usage by Country', 
                coloraxis_colorbar=dict(title='Internet Usage'), 
                coloraxis_colorbar_len=0.5, 
                coloraxis_colorbar_x=1.1, 
                margin={"r":0,"t":0,"l":0,"b":0}) 


st.plotly_chart(fig2)

