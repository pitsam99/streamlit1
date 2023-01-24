import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')
df=pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount in cr'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount in cr'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount in cr'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount in cr'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount in cr'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount in cr'])

    st.pyplot(fig3)



def load_investor_details(investor):
    st.title(investor)
#load the recent 5 investments of investor
    last5_df=df[df['investor'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount in cr']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1,col2= st.columns(2)

    with col1:

    # biggest investments
        big_series=df[df['investor'].str.contains(investor)].groupby('startup')['amount in cr'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values,color="maroon")

        st.pyplot(fig)
    with col2:
        verical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount in cr'].sum().sort_values(ascending=False).head()
        st.subheader('Top 5 Invested Sector')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series, labels=verical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)
    col1,col2=st.columns(2)
    with col1:
        invest_city=df[df['investor'].str.contains(investor)].groupby('city')['amount in cr'].sum()
        st.subheader('City Wise investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(invest_city, labels=invest_city.index, autopct="%0.01f%%")

        st.pyplot(fig1)
    with col2:
        round_invest = df[df['investor'].str.contains(investor)].groupby('round')['amount in cr'].sum()
        st.subheader('Investment Round')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_invest, labels=round_invest.index, autopct="%0.01f%%")
        st.pyplot(fig2)
    col1,col2= st.columns(2)
    with col1:
        invest_year = df[df['investor'].str.contains(investor)].groupby('year')['amount in cr'].sum()
        st.subheader('Investment Pattern')
        fig3, ax3 = plt.subplots()
        ax3.plot(invest_year.index,invest_year.values)
        st.pyplot(fig3)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('select One',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis' :
    load_overall_analysis()
elif option =='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox("Select Startup",sorted(set(df['investor'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2 :
        load_investor_details(selected_investor)
