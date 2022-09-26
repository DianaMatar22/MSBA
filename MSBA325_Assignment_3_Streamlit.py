from turtle import position
import tkinter as TK
import _tkinter
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly
import re
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
image = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/most-popular-video-games-of-2022-1642612227.png"
st.image(image, width=530)

df=pd.read_csv('vgsales.csv')
st.title('Video Games Sales Analysis')

page = st.sidebar.selectbox('Choose your topic',
  ['Global Sales of Video Games per Year','Sales By Region','Global Sales of Video Games by Platform',
  'Global Sales of Video Games by Publisher','Top 5 Publisher Video Game GLobal Sales by Year','Global Sales of Video Games by Genre'])

#Visualizing Global Sales per Year
if page == 'Global Sales of Video Games per Year':
    st.subheader("Global Sales of Video Games per Year")
    df_count_by_year = df.groupby(df['Year'])[['Rank']].count().rename(columns={'Rank':'counts'})
    df_sales_by_year = df.groupby(df['Year'])[['Global_Sales']].sum()
    fig1 = make_subplots()
    fig1.add_trace(
        go.Scatter(x=df_sales_by_year.index, y=df_sales_by_year['Global_Sales'], name='Global_Sales'),)
    fig1.update_xaxes(title_text="Year")
    fig1.update_yaxes(title_text="<b>Global Sales of Video Games</b>")
    st.plotly_chart(fig1)
    st.text(' -> From the above visualization, we notice that the sales of video games kept increasing from 1980 to reach its peak in 2008. It then started decreasing again. The graph shows that the data is not available after 2015.')

#Visualizing Sales by Region
if page == 'Sales By Region':
    st.subheader("Sales By Region")
    region_sec = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].apply(lambda x: x. sum (), axis = 0)
    region_sum = pd.DataFrame.from_dict(region_sec.to_dict(), orient = 'index', columns = ['sum']).sort_values('sum', ascending = False)
    fig2 = px.pie(region_sum , names=region_sum.index, values='sum', template='seaborn')
    fig2.update_traces(pull=[0,0.01,0.01,0.01],textinfo="percent+label")
    st.plotly_chart(fig2)
    st.text(' -> From the above visualization, we notice that the highest sales come from North America, followed by Europe, then Japan, and then other countries.')

#Visualizing Global Sales by Platform
if page == 'Global Sales of Video Games by Platform':
    st.subheader("Global Sales of Video Games by Platform")
    df_platform = df.groupby(df['Platform'])[['Global_Sales']].count().rename(columns = {'Global_Sales':'sales'}).sort_values('sales', ascending = False)
    fig3 = px.bar(df_platform, x=df_platform.index, y='sales', color='sales',color_continuous_scale=['rgba(248, 255, 148, 0.6)', 'rgba(209, 15, 18, 0.6)'],
                height=400)
    st.plotly_chart(fig3)
    st.text(' -> From the above visualization, we notice that the top 5 platforms with the highest sales are DS, PS2, PS3, Wii, and X360.')

#Visualizing Global Sales by Publisher
if page == 'Global Sales of Video Games by Publisher':
    st.subheader("Global Sales of Video Games by Publisher")
    df_publisher = df[:50].groupby(df['Publisher'])[['Global_Sales']].count().rename(columns = {'Global_Sales':'sales'}).sort_values('sales', ascending = False)
    fig4a = px.pie(df_publisher , names=df_publisher.index, values ='sales', template='seaborn')
    fig4a.update_traces(pull=[0.06,0.06,0.06,0.06,0.06], textinfo="percent+label")
    st.plotly_chart(fig4a)
    st.text(' -> As we notice in the pie chart, Nintendo has the biggest share of sales of Video Games and is the leading publishers in the industry, followed by Activision, Take-Two Interactive, Microsoft, and finally Sony.')

if page == 'Top 5 Publisher Video Game GLobal Sales by Year':
    st.subheader("Top 5 Publisher Video Game GLobal Sales by Year")
    top5_publishers = ['Nintendo', 'Sony Computer Entertainment','Microsoft Game Studios','Take-Two Interactive','Activision']
    perc = df.loc[:,["Year","Publisher",'Global_Sales']]
    perc['total_sales'] = perc.groupby([perc.Publisher,perc.Year])['Global_Sales'].transform('sum')
    perc.drop('Global_Sales', axis=1, inplace=True)
    perc = perc.drop_duplicates()
    perc = perc[(perc['Year']>=2006)]
    perc = perc.sort_values("Year",ascending = False)
    perc = perc.loc[perc['Publisher'].isin(top5_publishers)]
    perc = perc.sort_values("Year")
    fig4b=px.bar(perc,x ='Publisher', y ="total_sales", animation_frame="Year", 
            animation_group="Publisher", color="Publisher", hover_name ="Publisher",range_y=[0,200])
    st.plotly_chart(fig4b)
    st.text(' -> From the animated bar charts, we notice that Take-Two Interactive, and Sony are getting stronger and gaining more market share over the years.')

#Visualizing Global Sales by Genre
if page == 'Global Sales of Video Games by Genre':
    st.subheader("Global Sales of Video Games by Genre")
    df_genre = df.groupby(df['Genre'])[['Global_Sales']].count().rename(columns = {'Global_Sales':'sales'}).sort_values('sales', ascending = False)
    fig5 = px.bar(df_genre, x=df_genre.index, y='sales', color='sales',color_continuous_scale=['rgba(248, 255, 148, 0.6)', 'rgba(209, 15, 18, 0.6)'],
                height=400)
    st.plotly_chart(fig5)
    st.text(' -> From the above visualization, we notice that the top 5 genres with the highest sales are Action, Sports, Miscellenious, Role-Playing, and Shooter.')