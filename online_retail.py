#!/usr/bin/env python
# coding: utf-8

# # Portfolio Project: Online Retail Exploratory Data Analysis with Python

# ## Overview
# 
# In this project, you will step into the shoes of an entry-level data analyst at an online retail company, helping interpret real-world data to help make a key business decision.

# ## Case Study
# In this project, you will be working with transactional data from an online retail store. The dataset contains information about customer purchases, including product details, quantities, prices, and timestamps. Your task is to explore and analyze this dataset to gain insights into the store's sales trends, customer behavior, and popular products. 
# 
# By conducting exploratory data analysis, you will identify patterns, outliers, and correlations in the data, allowing you to make data-driven decisions and recommendations to optimize the store's operations and improve customer satisfaction. Through visualizations and statistical analysis, you will uncover key trends, such as the busiest sales months, best-selling products, and the store's most valuable customers. Ultimately, this project aims to provide actionable insights that can drive strategic business decisions and enhance the store's overall performance in the competitive online retail market.
# 
# ## Prerequisites
# 
# Before starting this project, you should have some basic knowledge of Python programming and Pandas. In addition, you may want to use the following packages in your Python environment:
# 
# - pandas
# - numpy
# - seaborn
# - matplotlib
# 
# These packages should already be installed in Coursera's Jupyter Notebook environment, however if you'd like to install additional packages that are not included in this environment or are working off platform you can install additional packages using `!pip install packagename` within a notebook cell such as:
# 
# - `!pip install pandas`
# - `!pip install matplotlib`

# ## Project Objectives
# 1. Describe data to answer key questions to uncover insights
# 2. Gain valuable insights that will help improve online retail performance
# 3. Provide analytic insights and data-driven recommendations

# ## Dataset
# 
# The dataset you will be working with is the "Online Retail" dataset. It contains transactional data of an online retail store from 2010 to 2011. The dataset is available as a .xlsx file named `Online Retail.xlsx`. This data file is already included in the Coursera Jupyter Notebook environment, however if you are working off-platform it can also be downloaded [here](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx).
# 
# The dataset contains the following columns:
# 
# - InvoiceNo: Invoice number of the transaction
# - StockCode: Unique code of the product
# - Description: Description of the product
# - Quantity: Quantity of the product in the transaction
# - InvoiceDate: Date and time of the transaction
# - UnitPrice: Unit price of the product
# - CustomerID: Unique identifier of the customer
# - Country: Country where the transaction occurred

# ## Tasks
# 
# You may explore this dataset in any way you would like - however if you'd like some help getting started, here are a few ideas:
# 
# 1. Load the dataset into a Pandas DataFrame and display the first few rows to get an overview of the data.
# 2. Perform data cleaning by handling missing values, if any, and removing any redundant or unnecessary columns.
# 3. Explore the basic statistics of the dataset, including measures of central tendency and dispersion.
# 4. Perform data visualization to gain insights into the dataset. Generate appropriate plots, such as histograms, scatter plots, or bar plots, to visualize different aspects of the data.
# 5. Analyze the sales trends over time. Identify the busiest months and days of the week in terms of sales.
# 6. Explore the top-selling products and countries based on the quantity sold.
# 7. Identify any outliers or anomalies in the dataset and discuss their potential impact on the analysis.
# 8. Draw conclusions and summarize your findings from the exploratory data analysis.

# ## Task 1: Load the Data

# In[7]:


import os
os.listdir('/home/jovyan/work/')


# In[8]:


import pandas as pd

path = '/home/jovyan/work/Online Retail.xlsx'
df = pd.read_excel(path)


# In[9]:


df.head()


# In[10]:


df.isnull()


# In[11]:


df.info()


# In[12]:


print(df.info())


# In[13]:


df.isnull().sum()


# In[15]:


df = df.dropna(subset=['Description'])
df['CustomerID'] = df['CustomerID'].fillna(0)


# In[16]:


df = df.drop(columns=['Unnamed: 0'], errors='ignore')


# In[17]:


df = df.drop_duplicates()


# In[18]:


print(df.describe())  # Summary statistics
print(df.info())      # Data types and missing values


# In[19]:


import matplotlib.pyplot as plt
import seaborn as sns

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) 
#converts invoicedate to date time format 2XXX-XX-X 08:00 for processing

df['Month'] = df['InvoiceDate'].dt.month 
#separating month in variable Month

monthly_sales = df.groupby('Month')['Quantity'].sum() #groupby month wise, quantity column and take sum of the quantity entities against each month

plt.figure(figsize=(10,5))

sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker='o', color='b')
#sns.lineplot() → Creates a line plot to visualize trends over time.
#x=monthly_sales.index → Sets the x-axis to the month numbers (from the index of monthly_sales).
#y=monthly_sales.values → Sets the y-axis to the total quantity sold in each month.
#marker='o' → Places circular markers (o) at each data point.
#color='b' → Uses blue (b) for the line and markers.

plt.title('Total Sales per Month')
plt.xlabel('Month')
plt.ylabel('Quantity Sold')
plt.show()


# In[20]:


top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
#1️⃣ df.groupby('Description')
    #Groups the dataset by product descriptions (i.e., unique product names).
    #This ensures that we aggregate sales for each product.

#2️⃣ ['Quantity'].sum()
    #For each product, it sums up the total quantity sold across all transactions.

#3️⃣ .sort_values(ascending=False)
    #Sorts the products in descending order (highest sales first).

#4️⃣ .head(10)
    #Retrieves the top 10 best-selling products.
    
plt.figure(figsize=(10,5))
sns.barplot(y=top_products.index, x=top_products.values, palette='viridis')
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Description')
plt.show()


# In[21]:


top_countries = df.groupby('Country')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
sns.barplot(y=top_countries.index, x=top_countries.values, palette='magma')
plt.title('Top 10 Countries by Sales')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Country')
plt.show()


# In[22]:


plt.figure(figsize=(8,5))
sns.boxplot(x=df['Quantity'])
plt.title('Boxplot of Quantity Sold')
plt.show()


# In[24]:


# Extract day of the week as a name
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()

# Aggregate sales per day of the week
weekly_sales = df.groupby('DayOfWeek')['Quantity'].sum()

# Sort days in correct order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_sales = weekly_sales.reindex(day_order)

# Plot
plt.figure(figsize=(10, 5))
sns.barplot(x=weekly_sales.index, y=weekly_sales.values, palette='viridis')
plt.title('Total Sales by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45)
plt.show()


# ## Final Analysis & Recommendations
# 
# ### Key Findings from Data Analysis
# 
# #### 1. Sales Trends Over Time (Monthly Sales)
# - Sales gradually increase from mid-year onward, peaking in **November** (Black Friday and holiday shopping).
# - Sales drop sharply in **December**, likely due to completed holiday shopping in November or stock shortages.
# - The slowest months are **January and February**, possibly due to post-holiday spending reductions.
# 
# ![Total Sales per Month](./Total_Sales_per_Month.png) 
# 
# **Recommendation:**
# - Increase **stock levels and marketing campaigns before Q4** to leverage peak demand.
# - Offer **early-bird holiday promotions in October** to spread out demand.
# - Introduce **post-holiday discounts** in January to boost slow-month sales.
# 
# #### 2. Busiest Days of the Week (Weekly Sales)
# - **Thursday is the busiest sales day**, followed by Tuesday and Wednesday.
# - **Weekends (especially Sunday) have the lowest sales**, possibly due to reduced business purchases.
# 
# ![Total Sales by Day of the Week](./Total_Sales_per_Day.png)  
# 
# **Recommendation:**
# - **Schedule major promotions on Thursdays** to maximize revenue.
# - Introduce **"Weekend Special" deals** to encourage more sales on Saturdays and Sundays.
# 
# #### 3. Best-Selling Products
# - The **top-selling product is "WORLD WAR 2 GLIDERS ASSORTED DESIGNS"**, followed by **"JUMBO BAG RED RETROSPOT"** and **"POPCORN HOLDER"**.
# - Many of the bestsellers are **small giftable items or novelty products**.
# 
# ![Top 10 Best-Selling Products](./Top_10_Best_Selling_Products.png)  
# 
# **Recommendation:**
# - Keep **high stock levels of best-selling items**, especially before peak sales periods.
# - Use **bundling strategies** (e.g., "Buy 2 Get 1 Free") to encourage bulk purchases of popular products.
# 
# #### 4. Top Countries by Sales
# - **The United Kingdom dominates sales**, far exceeding other countries.
# - The next highest sales come from the **Netherlands, Ireland, and Germany**, but at much lower levels.
# 
# ![Top Countries by Sales](./Top_Countries_by_Sales.png)  
# 
# **Recommendation:**
# - **Prioritize marketing and inventory for UK customers**, as they are the primary revenue source.
# - Expand targeted marketing in **Netherlands, Ireland, and Germany** to grow international sales.
# 
# #### 5. Outlier Detection (Boxplot Analysis)
# - There are **extreme outliers in the quantity sold**, with **some transactions showing negative values (returns/cancellations).**
# - Some transactions involve **very large bulk purchases**, which may indicate business buyers.
# 
# ![Boxplot of Quantity Sold](./Boxplot_Quantity_Sold.png)  
# 
# **Recommendation:**
# - Investigate **negative quantity values** to understand return patterns and reduce refund rates.
# - Introduce a **loyalty program for bulk buyers** to encourage repeat purchases.
# 
# ### Final Conclusion
# The online store experiences **strong seasonal trends**, with **peak sales in Q4 (November)** and **weaker sales in early months (January–February).** Sales also **vary by day of the week**, with **Thursday being the best sales day.** The UK is the **dominant market**, and the top-selling products are **giftable novelty items.**
# 
# By implementing **targeted marketing, strategic stock management, and seasonal promotions**, the store can **maximize revenue, optimize inventory, and enhance customer satisfaction.
# 

# In[ ]:




