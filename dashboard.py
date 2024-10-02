import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Bike Sharing Data Analysis')

# Load original data
day_df = pd.read_csv("bike_sharing_day.csv")
hour_df = pd.read_csv("bike_sharing_hour.csv")

# Doing some preprocessing based on google colab's work
# mostly just converting datatypes to thir proper type and accessing some specific values from them
# for example, getting just the year, or just the month, etc
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
day_df['year'] = day_df['dteday'].dt.year
day_df['month'] = day_df['dteday'].dt.month
day_df['day'] = day_df['dteday'].dt.day

# Peak Hour Rentals
st.subheader('Peak Hours for Bike Rentals')
peak_hour_df = hour_df.groupby(by='hr')['cnt'].sum().sort_values(ascending=False)
st.bar_chart(peak_hour_df)

# Peak Day Rentals
st.subheader('Peak Date for Bike Rentals (All Dates)')
peak_day_df = day_df.groupby(by="day")['cnt'].sum().sort_values(ascending=False)
st.bar_chart(peak_day_df)

# Peak Rentals per Quarter
# again, it's the same as the google colab's work
st.subheader('Peak Rentals per Quarter')
day_df['quarter'] = ((day_df['month'] - 1) // 3) + 1
peak_days_df = (
    day_df.loc[day_df.groupby(['year', 'quarter'])['cnt'].idxmax(), ['year', 'quarter', 'day', 'cnt']]
    .rename(columns={'day': 'highest_day'})
    .reset_index(drop=True)
)

# Plot for Peak Rentals per Quarter
fig, ax = plt.subplots(figsize=(10, 6))
for year in peak_days_df['year'].unique():
    data = peak_days_df[peak_days_df['year'] == year]
    ax.plot(data['quarter'], data['cnt'], marker='o', label=f'Year {year}')

ax.set_title('Peak Bike Rentals per Quarter')
ax.set_xlabel('Quarter')
ax.set_ylabel('Rental Count (cnt)')
ax.set_xticks([1, 2, 3, 4])
ax.legend(title='Year')
ax.grid(True)
st.pyplot(fig)

# Monthly Growth (Comparing Casual and Registered Customers) 
# previously, i kinda wanna do it based on it's percentage, but its kinda confusing (for me) so i just went with comparing the numbers
st.subheader('Monthly Growth of Customers (Casual vs Registered)')
monthly_growth_df = day_df.groupby(by=["year", "month"])[['casual', 'registered']].sum().reset_index()
monthly_growth_melted = monthly_growth_df.melt(id_vars=['year', 'month'],
                                                  value_vars=['casual', 'registered'],
                                                  var_name='Customer Type',
                                                  value_name='Number of Customers')

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=monthly_growth_melted,
            x="month",
            y="Number of Customers",
            hue="Customer Type",
            errorbar=None, ax=ax)

ax.set_title('Casual vs Registered Customers per Month')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Customers')
st.pyplot(fig)

# Seasonal Analysis
st.subheader('Seasonal Analysis')
season_cnt_df = day_df.groupby(by="season")['cnt'].sum().sort_values(ascending=False).reset_index()
st.bar_chart(season_cnt_df.set_index('season'))

# Weather vs Customers Correlation
st.subheader('Weather vs Customer Correlation')
weather_customer_df = day_df.groupby(by=["weathersit", "year"])['cnt'].sum().reset_index().sort_values(by="year")
st.write(weather_customer_df)

# Final Message
st.write("I am confusion D:")

