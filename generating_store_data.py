# generating_store_data.py
import numpy as np
import pandas as pd
import names
from faker import Faker
faker = Faker()
import pandasql as ps
import random
from datetime import datetime

def sql(query):
    return ps.sqldf(query)

'''
Generating Product Data
'''

# Load product data from sample CSV instead of web scraping
product_df = pd.read_csv('whisky_products.csv')
# Clean the Alcohol_Price column (remove currency symbols or commas if any)
product_df['Alcohol_Price'] = product_df['Alcohol_Price'].astype(str)\
    .str.replace('[,£]', '', regex=True).astype('float')

# Generate a column of unique product ids
product_id = np.random.default_rng().choice(len(product_df.Product_Name), 
                                           len(product_df.Product_Name), replace=False)
assert len(set(product_id)) == len(product_df.Product_Name)
assert len(pd.Series(product_id).unique()) == len(product_id)
product_df['product_id'] = product_id

'''
Generating Employee Data
'''

# 100 unique employee IDs
employee_id = np.random.default_rng().choice(4000, 100, replace=False)
assert len(set(employee_id)) == 100
assert len(pd.Series(employee_id).unique()) == len(employee_id)

departments = ['Sales', 'Finance', 'Marketing', 'BI']
employee_data = {
    'employee_id': [],
    'first_name': [],
    'last_name': [],
    'full_name': [],
    'email': [],
    'city': [],
    'department': []
}

for i in range(len(employee_id)):
    first = names.get_first_name()
    last = names.get_last_name()
    employee_data['employee_id'].append(employee_id[i])
    employee_data['first_name'].append(first)
    employee_data['last_name'].append(last)
    employee_data['full_name'].append(f"{first} {last}")
    employee_data['email'].append(f"{first}{last[0].lower()}@gmail.com")
    employee_data['city'].append(faker.city())
    employee_data['department'].append(np.random.choice(departments))

employee_df = pd.DataFrame(employee_data)

'''
Generating Customer Data
'''

# 1000 unique customer IDs
customer_id = np.random.default_rng().choice(999999, 1000, replace=False)
assert len(set(customer_id)) == 1000
assert len(pd.Series(customer_id).unique()) == len(customer_id)

customer_data = {
    'customer_id': [],
    'first_name': [],
    'last_name': [],
    'full_name': [],
    'email': [],
    'country': [],
    'country_code': [],
    'street': [],
    'credit_provider': [],
    'four_digits': []
}

for i in range(len(customer_id)):
    first = names.get_first_name()
    last = names.get_last_name()
    country = faker.country()
    country_code = country[:3].upper()
    customer_data['customer_id'].append(customer_id[i])
    customer_data['first_name'].append(first)
    customer_data['last_name'].append(last)
    customer_data['full_name'].append(f"{first} {last}")
    customer_data['email'].append(f"{first}{last[0].lower()}@gmail.com")
    customer_data['country'].append(country)
    customer_data['country_code'].append(country_code)
    customer_data['street'].append(faker.street_address())
    customer_data['credit_provider'].append(faker.credit_card_provider())
    customer_data['four_digits'].append(np.random.randint(1000, 9999))

customer_df = pd.DataFrame(customer_data)

'''
Generating Payments Data
'''

date_range = pd.date_range(start="1990-01-01", end="2020-12-31", freq="D")
payment_id = np.random.default_rng().choice(999999, len(date_range), replace=False)
assert len(set(payment_id)) == len(date_range)
assert len(pd.Series(payment_id).unique()) == len(payment_id)

payment_data = {
    'payment_id': [],
    'date': [],
    'customer_id': [],
    'employee_id': [],
    'product_id': []
}

for pid in payment_id:
    payment_data['payment_id'].append(pid)
    payment_data['date'].append(datetime.strftime(random.choice(date_range), '%Y-%m-%d'))
    payment_data['customer_id'].append(random.choice(customer_id))
    payment_data['employee_id'].append(random.choice(employee_id))
    payment_data['product_id'].append(random.choice(product_id))

payment_df = pd.DataFrame(payment_data)

# Add Alcohol_Price to payments by joining on product_id
query = '''
select p1.*, p2.Alcohol_Price as price
from payment_df p1
inner join product_df p2
on p1.product_id = p2.product_id
'''
payment_df = sql(query)

# Save all dataframes to CSV for subsequent steps
product_df.to_csv('products.csv', index=False)
employee_df.to_csv('employees.csv', index=False)
customer_df.to_csv('customers.csv', index=False)
payment_df.to_csv('payments.csv', index=False)
