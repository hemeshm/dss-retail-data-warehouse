# normalize_data.py
import pandas as pd
import pandasql as ps

# Load generated data from CSV
customer_df = pd.read_csv('customers.csv')
employee_df = pd.read_csv('employees.csv')

def sql(query):
    return ps.sqldf(query)

'''
Normalizing the Customers Table
'''

# Create countries table
unique_countries = customer_df.country.unique()
countries_df = pd.DataFrame(unique_countries, columns=['Country'])
countries_df['Country_Code'] = countries_df.Country.str[:3].str.upper()
countries_df['country_id'] = range(len(countries_df))

# Assign country_id to customers
query = '''
select countries_df.country_id
from customer_df 
join countries_df
on customer_df.country_code = countries_df.Country_Code
'''
country_ids = sql(query).country_id
customer_df['country_id'] = country_ids
customer_df = customer_df.drop(['country','country_code'], axis=1)

'''
Customer Credit Providers
'''
unique_cc = customer_df.credit_provider.unique()
customer_cc_df = pd.DataFrame(unique_cc, columns=['credit_provider'])
customer_cc_df['credit_provider_id'] = range(len(customer_cc_df))

query = '''
select customer_cc_df.credit_provider_id
from customer_df
join customer_cc_df
on customer_df.credit_provider = customer_cc_df.credit_provider
'''
cc_ids = sql(query).credit_provider_id
customer_df['credit_provider_id'] = cc_ids
customer_df = customer_df.drop(['credit_provider'], axis=1)

'''
Normalizing the Employees Table
'''
departments = employee_df.department.unique().tolist()
department_df = pd.DataFrame({'department': departments})
department_df['department_id'] = range(len(department_df))

query = '''
select department_df.department_id
from employee_df
join department_df
on employee_df.department = department_df.department
'''
dept_ids = sql(query).department_id
employee_df['department_id'] = dept_ids
employee_df = employee_df.drop('department', axis=1)

# Save normalized tables and updated dataframes
countries_df.to_csv('countries.csv', index=False)
customer_cc_df.to_csv('customer_cc.csv', index=False)
department_df.to_csv('departments.csv', index=False)
customer_df.to_csv('customers_norm.csv', index=False)
employee_df.to_csv('employees_norm.csv', index=False)
