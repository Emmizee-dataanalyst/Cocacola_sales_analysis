import pandas as pd 
import streamlit as st 

st.title("COCACOLA SALES PERFORMANCE ANALYSIS")

cola = pd.read_excel("cleaned_cola_data.xlsx")
# st.dataframe(cola)

filters = {

"Retailer": cola["Retailer"].unique(),
"Region": cola["Region"].unique(),
"Beverage Brand": cola["Beverage Brand"].unique(),
"State": cola["State"].unique(),
"Operating margin(%)": cola["Operating margin(%)"].unique()
}

selected_filters = {}

for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key,options)

filtered_cola = cola.copy()

for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_cola = filtered_cola[filtered_cola[key].isin(selected_values)]


# st.dataframe(filtered_cola)

#st.dataframe(cola)

# Calculations

Total_Sales = filtered_cola["Total Sales"].sum()
Total_Units_Sold = filtered_cola["Units Sold"].sum()
Total_Profits = filtered_cola["Operating Profit"].sum()
No_of_Beverage_brands = filtered_cola["Beverage Brand"].nunique()
Average_margin = filtered_cola["Operating Margin"].mean()

st.write("### Quick Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Sales: ", f"${Total_Sales:,.2f}")
with col2:
    st.metric("Total Units Sold: ", f"{Total_Units_Sold:,.0f}")
with col3:
    st.metric("Total Profits: ", f"${Total_Profits:,.2f}")
with col4:
    st.metric("Beverage Brands: ", No_of_Beverage_brands)
with col5:
    st.metric("Average Operating Margin: ", f"{Average_margin:.2%}")

st.write("### Analysis Findings")

st.write("#### 1. Beverage Brand with the most Sales")

temp_1 = filtered_cola.groupby('Beverage Brand')['Total Sales'].sum().sort_values(ascending=False)
temp_1.columns = ["Beverage Brand", "Total Sales"]

st.dataframe(temp_1)

import altair as alt 

sales_chart = alt.Chart(filtered_cola).mark_bar().encode(
    x=alt.X('Beverage Brand:N', sort='-y'),
    y='sum(Total Sales):Q',
    color='Beverage Brand:N',
    tooltip=['Beverage Brand', alt.Tooltip('sum(Total Sales):Q', format='$,.2f')]
).properties(width=600)
st.altair_chart(sales_chart, use_container_width=True)

st.write("#### 2. Beverage Brands with the most profits")

temp_2 = filtered_cola.groupby('Beverage Brand')['Operating Profit'].sum().reset_index()
temp_2 = temp_2.sort_values(by='Operating Profit', ascending=False)

st.dataframe(temp_2)

profit_chart = alt.Chart(temp_2).mark_bar().encode(
    y=alt.Y('Beverage Brand:N', sort='-x'),  # Beverage brands on Y-axis
    x=alt.X('Operating Profit:Q'),           # Profit on X-axis
    color='Beverage Brand:N',
    tooltip=[
        'Beverage Brand',
        alt.Tooltip('Operating Profit:Q', format='$,.2f')
    ]
).properties(width=600)

st.altair_chart(profit_chart, use_container_width=True)

st.write("#### 3. Beverage Brands by most units sold")

temp_3 = filtered_cola.groupby('Beverage Brand')['Units Sold'].sum().sort_values(ascending=False) 

temp_3_filtered_cola = temp_3.reset_index()
temp_3_filtered_cola.columns = ['State', 'Units Sold']

# Example stacked chart — adding a fake category just to illustrate
temp_3_filtered_cola['Category'] = ['A' if i % 2 == 0 else 'B' for i in range(len(temp_3_filtered_cola))]

# Create stacked bar chart
chart = alt.Chart(temp_3_filtered_cola).mark_bar().encode(
    x=alt.X('State', sort='-y'),
    y='Units Sold',
    color='Category',  # This is what creates the stacked effect
    tooltip=['State', 'Category', 'Units Sold']
).properties(
    width=600,
    height=400,
    title="Units Sold per State (Stacked)"
)

chart

st.write("### 4. Monthly Sales Trend")

filtered_cola['Month'] = cola['Invoice Date'].dt.to_period('M').astype(str)
temp_4 = filtered_cola.groupby(['Month', 'Beverage Brand'])['Total Sales'].sum().reset_index()
temp_4.columns = ["Month", "Beverage Brand", "Total Sales"]

st.dataframe(temp_4)

monthly_sales_chart = alt.Chart(filtered_cola).mark_line(point=True).encode(
    x='Month:T',
    y='sum(Total Sales):Q',
    color='Beverage Brand:N',
    tooltip=['Beverage Brand', 'Month', alt.Tooltip('sum(Total Sales):Q', format='$,.2f')]
).properties(width=700)
st.altair_chart(monthly_sales_chart, use_container_width=True)


st.write("#### 5. Location Trend by Units Sold")

temp_5 = filtered_cola.groupby('State')['Units Sold'].sum().reset_index().sort_values(by='Units Sold', ascending=False)
temp_5.columns = ["State", "Units Sold"]

st.dataframe(temp_5)

chart = alt.Chart(temp_5).mark_circle().encode(
    x=alt.X('State:N', sort='-y', title='State'),
    y=alt.Y('Units Sold:Q', title='Units Sold'),
    size=alt.Size('Units Sold:Q', scale=alt.Scale(range=[100, 2000])),
    color=alt.Color('Units Sold:Q', scale=alt.Scale(scheme='blues')),
    tooltip=['State', 'Units Sold']
).properties(
    title='Units Sold by State',
    width=600,
    height=400
).interactive()

chart

st.write("### 6. Beverage Brands with the most operating margin")

temp_6 = filtered_cola.groupby('Beverage Brand')['Operating Margin'].mean().sort_values(ascending=False)
temp_6.columns = ["Beverage Brand", "Operating margin"]

st.dataframe(temp_6)

margin_chart = alt.Chart(filtered_cola).mark_bar().encode(
    x=alt.X('Beverage Brand:N', sort='-y'),
    y='mean(Operating Margin):Q',
    color='Beverage Brand:N',
    tooltip=['Beverage Brand', alt.Tooltip('mean(Operating Margin):Q', format='.2%')]
).properties(width=600)
st.altair_chart(margin_chart, use_container_width=True)

st.write("#### 7. Monthly trend by units sold")

filtered_cola['Month'] = filtered_cola['Invoice Date'].dt.to_period('M').astype(str)

temp_7 = filtered_cola.groupby('Month')['Units Sold'].sum().reset_index().sort_values(by='Units Sold', ascending=False)
temp_7.columns = ["Month", "Units Sold"]

st.dataframe(temp_7)

chart = alt.Chart(temp_7).mark_area().encode(
    x=alt.X('Month:N', sort=None, title='Month'),
    y=alt.Y('Units Sold:Q', title='Units Sold'),
    tooltip=['Month', 'Units Sold']
).properties(
    title='Units Sold by Month'
).interactive()

chart
