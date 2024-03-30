
#%%
#####################
##Import of Modules##
#####################

import pandas as pd
import numpy as np
import streamlit as st

#%%
#######################
# Data import & columns
#######################

df = pd.read_csv('fpldata.csv') #locally saved file imported here as read into dataframe - "df" - FPL 20/21 data

#%%

df.head()  #to have a look at top entries and columns / rows  of  table could have used .columns  etc too

#%%
# Trying to calculate dynamic metrics at per miinute levels for better analysis

df['90s'] = df['minutes']/90  #per match / proxy 90 minute column creation

calc_elements = ['goals', 'assists', 'points'] #dynamic metrics which needs to be transformed

#%%
#For loop to create 3 different column/metrics in table
for each in calc_elements:
    df[f'{each}_p90'] = df[each] / df['90s']

#%%
#Having a look at unique elements to provide for filteration criteria during analysis
positions = list(df['position'].drop_duplicates())
teams = list(df['team'].drop_duplicates())

#%%
########################################################
# App design - now use of streamlit library coming ahead
########################################################

# Sidebar - title & filters - Here we are creating filters for onscreen selection and  hence will use these in the filteration from dataframe as  well upon selection
st.sidebar.markdown('Data Filters')                                 #Gives title to  sidebar top
position_choice = st.sidebar.multiselect(                           #declares a variable which will store entries from streamlit frontend 
    'Choose position:', positions, default=positions)
teams_choice = st.sidebar.multiselect(
    "Teams:", teams, default=teams)
price_choice = st.sidebar.slider(
    'Max Player Cost:', min_value=4.0, max_value=15.0, step=.5, value=15.0)

#%%
#############################################################################################################
#Filters use to trim down our  dataframe to  give results which we committed above by the frontend selections
#############################################################################################################

df = df[df['position'].isin(position_choice)]  #can use isin or == could be many ways  to ddo similar stuff
df = df[df['team'].isin(teams_choice)]
df = df[df['cost'] < price_choice]

#%%

#########################
# Main Dashboard creation
#########################

st.title(f"EPL - Fantasy Football Fun Zone")

#########################
# Main - dataframes
#########################

st.markdown('Player Stats')

st.dataframe(df.sort_values('points',
             ascending=False).reset_index(drop=True)) #could have been passed normally just for asthetic purpose done

#display plots and images from loads of different sources. Local images, Matplotlib plots, the Plotly library and more (check the docs). In this example, we’ll use a really nice library called vega-lite. Vega-lite is a javascript library

#%%
#############################################################################################################################
# Main - charts - We have used vega lite  Javascript Library here as we told above as well which streamlit helps us use here
#############################################################################################################################

#2 types of charts created here at first. Will be adding more as per the analysis expansion

#1
st.markdown('Player Cost vs Points')

st.vega_lite_chart(df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'cost', 'type': 'quantitative'},
        'y': {'field': 'points', 'type': 'quantitative'},
        'color': {'field': 'position', 'type': 'nominal'},
        'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
    },
    'width': 700,
    'height': 400,
})

#%%
#2
st.markdown('Goals per 90  mins vs Assists per 90 mins')

st.vega_lite_chart(df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'goals_p90', 'type': 'quantitative'},
        'y': {'field': 'assists_p90', 'type': 'quantitative'},
        'color': {'field': 'position', 'type': 'nominal'},
        'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
    },
    'width': 700,
    'height': 400,
})

# %%
