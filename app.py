import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("retail_dashboard_ready.csv")


st.title("Retail Sales Dashboard")

#slicers
region = st.multiselect("Select Region:", df["Region"].unique(), default=df["Region"].unique())
category = st.multiselect("Select Product Category:", df["ProductCategory"].unique(), default=df["ProductCategory"].unique())
gender = st.multiselect("Select Gender:", df["Gender"].unique(), default=df["Gender"].unique())

# Apply filters
filtered_df = df[df["Region"].isin(region) & df["ProductCategory"].isin(category) & df["Gender"].isin(gender)]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{filtered_df['TotalSpent'].sum():,.2f}")
col2.metric("Avg Spend/Item", f"{filtered_df['SpendingPerItem'].mean():.2f}")
col3.metric("Total Quantity", int(filtered_df['Quantity'].sum()))

# Sales by Product Category

st.subheader("Sales by Product Category")
fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_df, x="ProductCategory", y="TotalSpent", estimator=sum, ax=ax1)
ax1.set_ylabel("Total Sales")
st.pyplot(fig1)

# Sales over time (by month)
st.subheader(" Monthly Sales Trend")
monthly_sales = filtered_df.groupby("Month")["TotalSpent"].sum().reindex(range(1, 13), fill_value=0)
fig2, ax2 = plt.subplots()
monthly_sales.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Total Sales")
st.pyplot(fig2)

# Boxplot by AgeGroup
st.subheader(" Spending by Age Group")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x="AgeGroup", y="TotalSpent", ax=ax3)
ax3.set_ylabel("Total Sales")
st.pyplot(fig3)

# Pie Chart: Sales by Region
st.subheader(" Sales Distribution by Region")
region_sales = filtered_df.groupby("Region")["TotalSpent"].sum()
fig4, ax4 = plt.subplots()
ax4.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%')
ax4.axis('equal')
st.pyplot(fig4)
