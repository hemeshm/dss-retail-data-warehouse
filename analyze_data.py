# analyze_data.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
import pandasql as ps
from empiricaldist import Pmf

plt.style.use('ggplot')
sns.set_palette('Blues_r')
sns.set_context('notebook')

def mysql(query):
    return pd.read_sql_query(query, connection)

def sql(query):
    return ps.sqldf(query)

# Connect to MySQL database
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='dss_user0',
    passwd='73841A',
    db='retail_dss0'
)
cursor = connection.cursor()

# Pulling Data
query = '''
select 
    f.date,
    d.Day_name as Day,
    d.Month_name as Month,
    d.Year_name as Year,
    f.Product_Name,
    f.Alcohol_Price,
    f.Alcohol_Percent,
    f.Alcohol_Amount,
    c.full_name as customer_name,
    co.Country as customer_country,
    f.credit_provider,
    e.full_name as employee_name
from dwh_fact as f
left join whiskey_retail_shop.customers c
    on f.customer_id = c.customer_id
left join whiskey_retail_shop.countries as co
    on co.country_id = c.country_id 
left join dwh_employees as e
    on e.employee_id = f.employee_id
left join dwh_date d
    on d.Date_key = f.Date_key
order by f.date
'''
df = mysql(query)

# Preprocessing
for column in df.columns:
    if column == 'date':
        df[column] = pd.to_datetime(df[column])
    if df[column].dtype == 'object':
        df[column] = df[column].astype('category')

# Q1 - Top 5 Most Profitable Products
query = '''
select 
    count(*) as Number_Of_Transactions, 
    Product_Name, 
    sum(Alcohol_Price) as Profit
from df
group by Product_Name
order by sum(Alcohol_Price) desc
limit 5
'''
top_5_products = sql(query)

sns.catplot(data=top_5_products, x='Product_Name', y='Profit', kind='bar', palette='Blues_r', height=6, aspect=2)
plt.xlabel('Product Name', size=16)
plt.ylabel('Profit', size=16)
plt.title('Top 5 Most Profitable Products', size=18)
plt.tight_layout()
plt.show()

# Q2 - Probability to Buy (Top Products)
prob_mass_func = pd.DataFrame(Pmf.from_seq(df.Product_Name))
sorted_prob_mass_func = prob_mass_func.iloc[:, 0].sort_values(ascending=False)
sorted_prob_mass_func = sorted_prob_mass_func[sorted_prob_mass_func > sorted_prob_mass_func.quantile(0.95)]

probability_df = pd.DataFrame({
    'Product': sorted_prob_mass_func.index,
    'Probability to Buy': sorted_prob_mass_func.values
})
print("\nProbability to Buy (Top Products):")
print(probability_df)

# Q3 - Transactions by Day of Week
query = '''
select 
    count(*) as Number_Of_Transactions, 
    Day
from df
group by Day
order by count(*) desc
'''
most_by_day = sql(query)

sns.catplot(data=most_by_day, y='Number_Of_Transactions', x='Day', kind='bar', height=6, aspect=3)
plt.xlabel('Day of Week', size=18)
plt.ylabel('Number of Transactions', size=18)
plt.title('Transactions by Day of Week', size=20)
plt.tight_layout()
plt.show()

# Q4 - Yearly Profit Growth
query = '''
select 
    sum(Alcohol_Price) as Profit, 
    Year
from df
where Year != 2022
group by Year
order by Year asc
'''
profits_by_year = sql(query)

x = profits_by_year.Year
y = np.cumsum(profits_by_year.Profit)

plt.figure(figsize=(15, 8))
plt.plot(x, y, marker='o')
plt.xlabel('Year', size=16)
plt.ylabel('Cumulative Profit', size=16)
plt.title('Cumulative Profit by Year', size=20)
plt.grid(True)
plt.tight_layout()
plt.show()

# Q5 - Top Countries by Number of Customers
query = '''
select 
    count(distinct customer_name) as Number_of_Customers, 
    customer_country
from df
group by customer_country
order by Number_of_Customers desc
'''
customers_by_country = sql(query)
top_ten = customers_by_country.head(int(len(customers_by_country) * 0.1))

print("\nTop Countries by Number of Customers:")
print(top_ten)

sns.barplot(data=top_ten, x='Number_of_Customers', y='customer_country')
plt.xlabel('Number of Customers')
plt.ylabel('Country')
plt.title('Top Countries by Number of Customers')
plt.tight_layout()
plt.show()
